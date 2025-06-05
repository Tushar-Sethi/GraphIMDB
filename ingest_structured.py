"""
Reads IMDb TSVs (title.basics.tsv, title.ratings.tsv, name.basics.tsv, title.principals.tsv)
and ingests each movie as one JSON episode. Graphiti Core will automatically infer:
  - Movie nodes (fields: tconst, title, year, average_rating)
  - Genre nodes + HAS_GENRE edges
  - Person nodes + ACTED_IN / DIRECTED edges
No manual create_node or create_edge calls are needed.
"""

import pandas as pd
from graph_client import get_client
from graphiti_core.nodes import EpisodeType
import json
from datetime import datetime, timezone

# Paths to your IMDb TSV files (adjust if they live elsewhere)
TITLE_BASICS_PATH     = "./data/title.basics.tsv/titles.basics.tsv"
TITLE_RATINGS_PATH    = "./data/title.ratings.tsv/titles.ratings.tsv"
NAME_BASICS_PATH      = "./data/name.basics.tsv/names.basics.tsv"
TITLE_PRINCIPALS_PATH = "./data/title.principals.tsv/titles.principals.tsv"

# Prefix for episode names (for provenance/tracking)
EPISODE_PREFIX = "imdb_structured_import"

graphiti = get_client()

import os
print(os.getcwd())


def ingest_structured():
    
    # 1) Load all four TSVs into DataFrames
    
    basics     = pd.read_csv(TITLE_BASICS_PATH, sep="\t", na_values=["\\N"], dtype=str)
    
    ratings    = pd.read_csv(TITLE_RATINGS_PATH, sep="\t", na_values=["\\N"], dtype=str)
    
    names      = pd.read_csv(NAME_BASICS_PATH, sep="\t", na_values=["\\N"], dtype=str)
    
    principals = pd.read_csv(TITLE_PRINCIPALS_PATH, sep="\t", na_values=["\\N"], dtype=str)
    


    # 2) Merge basics + ratings so each movie row has its rating attached
    movies = basics.merge(ratings, on="tconst", how="left").fillna("")
    # Keep only actual movies (titleType == "movie")
    movies = movies[movies["titleType"] == "movie"]

    # 3) For each movie, build a single JSON episode
    episodes = []
    count = 0
    for _, row in movies.iterrows():

        count += 1
        tconst     = row["tconst"]
        title      = row["primaryTitle"]
        year       = int(row["startYear"]) if row["startYear"].isdigit() else None
        avg_rating = float(row["averageRating"]) if row["averageRating"] != "" else None

        # 3a) Extract genres as a list of strings (or [] if missing)
        genres = row["genres"].split(",") if row["genres"] else []

        # 3b) Filter `principals` DataFrame for this tconst
        pr = principals[principals["tconst"] == tconst]
        actor_ids    = pr[pr["category"].isin(["actor", "actress"])]["nconst"].tolist()
        director_ids = pr[pr["category"] == "director"]["nconst"].tolist()

        # 3c) Map nconst → primaryName via the names DataFrame
        actors   = names[names["nconst"].isin(actor_ids)]["primaryName"].tolist()
        directors = names[names["nconst"].isin(director_ids)]["primaryName"].tolist()

        # 4) Build JSON episode body
        episode_body = {
            "tconst": tconst,
            "title": title,
            "year": year,
            "average_rating": avg_rating,
            "genres": genres,
            "actors": actors,
            "directors": directors,
        }
        

        episodes.append({
            "content":episode_body,
            "type": EpisodeType.json,
            "description": f"IMDB structured data for {title} ({year}) for Genre {genres}"
            
        })
        
        graphiti.add_episode(
            name=f"{EPISODE_PREFIX}::{count}",
            episode_body=episode_body
            if isinstance(episode_body, str)
            else json.dumps(episode_body),
            source=EpisodeType.json,
            source_description=f"IMDB structured data for {title} ({year}) for Genre {genres}",
            reference_time=datetime.now(timezone.utc),
        )
        print('Episode added-----------------')

    print('Done with building JSON episodes --------------------------')
    print('episodes length-----------------',len(episodes))

if __name__ == "__main__":
    ingest_structured()
