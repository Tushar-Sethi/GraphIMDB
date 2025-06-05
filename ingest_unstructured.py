import pandas as pd
from graph_client import client
# Optional: import spacy for NER (if installed)
# import spacy

PLOTS_CSV_PATH = "data/plots.csv"    # columns: tconst, plot
REVIEWS_CSV_PATH = "data/reviews.csv"  # columns: review_id, tconst, author, date, review_text

# If using spaCy for NER:
# nlp = spacy.load("en_core_web_sm")


def ingest_unstructured():
    # 1) Ingest plot summaries directly onto Movie nodes
    plots = pd.read_csv(PLOTS_CSV_PATH, dtype=str)
    for _, row in plots.iterrows():
        client.update_node(
            "Movie", match={"tconst": row["tconst"]}, updates={"plot_summary": row["plot"]}
        )

    # 2) Ingest reviews as separate nodes and link to Movie
    reviews = pd.read_csv(REVIEWS_CSV_PATH, dtype=str)
    for _, row in reviews.iterrows():
        client.create_node("Review", {"review_id": row["review_id"], "text": row["review_text"]})
        client.create_edge("HAS_REVIEW", {"from": {"tconst": row["tconst"]}, "to": {"review_id": row["review_id"]}})

        # Optional: NER-based person mention linking
        # doc = nlp(row["review_text"])
        # for ent in doc.ents:
        #     if ent.label_ == "PERSON":
        #         # Attempt to match ent.text against Person nodes
        #         # This is a simple example using exact match or simple fuzzy matching
        #         matches = client.search_nodes("Person", {"name": ent.text})
        #         for person_node in matches:
        #             client.create_edge(
        #                 "MENTIONS_PERSON_IN_REVIEW",
        #                 {"from": {"nconst": person_node['nconst']}, "to": {"review_id": row["review_id"]}}
        #             )

    print("Unstructured data ingestion complete.")