from graph_client import get_client
from zep_memory import store_user_turn, store_bot_turn, fetch_last_message
from ollama_LLM import ollama_generate

graph_client = get_client()

async def chat_loop(session_id: str, user_message: str) -> str:
    # 1) Store user message in Zep memory
    store_user_turn(session_id, user_message)

    # 2) Retrieve only the last message for context
    last_msg = fetch_last_message(session_id)
    memory_text = f"Previous turn:\n{last_msg}\n" if last_msg else ""

    # graph_instructions = "NO_GRAPH_QUERY"
    # if "Christopher Nolan" in user_message and "direct" in user_message.lower():
    #     graph_instructions = (
    #         'MATCH (p:Person {name: "Christopher Nolan"})-[:DIRECTED]->(m:Movie) '
    #         'RETURN m.title AS title, m.year AS year, m.average_rating AS rating '
    #         'ORDER BY m.average_rating DESC LIMIT 10'
    #     )
    # elif "science fiction" in user_message.lower() and "top" in user_message.lower():
    #     graph_instructions = (
    #         'MATCH (m:Movie)-[:HAS_GENRE]->(g:Genre {name: "Sci-Fi"}) '
    #         'RETURN m.title AS title, m.year AS year, m.average_rating AS rating '
    #         'ORDER BY m.average_rating DESC LIMIT 5'
    #     )
    
    cypher_prompt = (
        "You are a helper that translates natural-language requests into Cypher queries. "
        "Given a user request about movies, people, genres, or reviews, output exactly one Cypher query "
        "that answers it. If the request does not require querying the graph, respond with NO_GRAPH_QUERY.\n\n"
        f"Example requests:\n"
        "- \"List all Christopher Nolan films sorted by rating desc\":\n"
        "  MATCH (p:Person {name: \"Christopher Nolan\"})-[:DIRECTED]->(m:Movie) "
        "RETURN m.title AS title, m.year AS year, m.average_rating AS rating "
        "ORDER BY m.average_rating DESC\n"
        "- \"Show me the plot summary of Inception\":\n"
        "  MATCH (m:Movie {title: \"Inception\"}) RETURN m.plot_summary AS plot\n"
        "- \"What is 2 + 2?\":\n"
        "  NO_GRAPH_QUERY\n\n"
        f"Now translate this request:\n\"{user_message}\""
    )
    graph_instructions = ollama_generate(cypher_prompt).strip()
    

    # 4) Execute graph query if needed
    try:
        graph_result_text = ""
        if graph_instructions != "NO_GRAPH_QUERY":
            subgraph = await graph_client.search(graph_instructions)
            
            bullets = []
            async for row in subgraph:
                title = row['properties'].get("title")
                year = row['properties'].get("released")
                tagline = row['properties'].get("tagline")
                bullets.append(f"- {title} ({year}) — Rating: {tagline}")
            
            graph_result_text = "Graph Results:\n" + "\n".join(bullets) + "\n"
    except:
        import traceback
        print(traceback.format_exc())

    # 5) Build LLM prompt
    prompt_sections = []
    if memory_text:
        prompt_sections.append(f"Previously in this conversation:\n{memory_text}\n")
    if graph_result_text:
        prompt_sections.append(graph_result_text)
    prompt_sections.append(f"User: {user_message}\nAssistant:")

    llm_prompt = "\n---\n".join(prompt_sections)
    # 6) Call Ollama via generate function
    assistant_response = ollama_generate(llm_prompt)

    # 7) Store assistant’s reply in memory
    store_bot_turn(session_id, assistant_response)
    return assistant_response
