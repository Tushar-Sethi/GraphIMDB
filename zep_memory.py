from zep_cloud.client import Zep
from zep_cloud.types import Message
import os
from dotenv import load_dotenv
load_dotenv()

ZEP_API_KEY = os.getenv("ZEP_API_KEY")



if not ZEP_API_KEY:
    raise RuntimeError("Please set the ZEP_API_KEY environment variable to your Zep Cloud API key.")

# Initialize Zep Cloud client
zep = Zep(api_key=ZEP_API_KEY)

COLLECTION_NAME = "chat_memory"

# Functions to store and fetch memory

def store_user_turn(session_id: str, user_text: str):
    msg = Message(role="user", content=user_text, role_type="user")
    zep.memory.add(session_id=session_id, messages=[msg])


def store_bot_turn(session_id: str, bot_text: str):
    msg = Message(role="assistant", content=bot_text, role_type="assistant")
    zep.memory.add(session_id=session_id, messages=[msg])


def fetch_last_message(session_id: str) -> str:
    """
    Retrieve the single most-recent message content for the given session.
    Returns an empty string if no messages exist.
    """
    memory = zep.memory.get(session_id=session_id)
    if not memory.messages:
        return ""
    
    return memory.messages[-2].content