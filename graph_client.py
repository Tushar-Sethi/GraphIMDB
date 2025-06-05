import os
from dotenv import load_dotenv
load_dotenv()

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

if not (NEO4J_URI and NEO4J_USER and NEO4J_PASSWORD):
    raise RuntimeError(
        "Please set the environment variables NEO4J_URI, NEO4J_USER, and NEO4J_PASSWORD.\n"
        "For example:\n"
        "  export NEO4J_URI=\"bolt://localhost:7687\"\n"
        "  export NEO4J_USER=\"neo4j\"\n"
        "  export NEO4J_PASSWORD=\"your_password\""
    )

# Import Graphiti Core
try:
    from graphiti_core import Graphiti
except ImportError as e:
    raise ImportError(
        "Cannot import Graphiti from 'graphiti_core'.\n"
        "Make sure you installed graphiti-core:\n"
        "    pip install graphiti-core\n"
        "If the error persists, check your Python environment."
    ) from e

graphiti = Graphiti(
    uri=NEO4J_URI,
    user=NEO4J_USER,
    password=NEO4J_PASSWORD,
)

def get_client():
    """
    Return the initialized GraphClient instance.
    Use client.add_episode(...) or client.raw_query(...) as needed.
    """
    return graphiti
