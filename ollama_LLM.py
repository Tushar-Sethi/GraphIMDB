import requests

def ollama_generate(prompt: str) -> str:
    resp = requests.post(
        "http://localhost:11434/api/generate",
        json={"model":"gemma3:1b","prompt":prompt,"stream":False},
    )
    resp.raise_for_status()
    return resp.json()["response"]