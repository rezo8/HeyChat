import random

from rag.vector_store import build_character
from llm.chat_generator import generate_chat_response

# Define your character's name, description, and data folder
CHARACTER_NAME = "Moderator"
CHARACTER_DESCRIPTION = "A quirky, sometimes biased, sometimes funny chat moderator."
DATA_FOLDER = "./data/moderator"

# Build the character's vector store collection
moderator_collection = build_character(
    name=CHARACTER_NAME, description=CHARACTER_DESCRIPTION, dataFolderPath=DATA_FOLDER
)


# Example: function to get relevant responses for a user message
def moderate_message(user_message, joke_chance=0.4):
    query = f"Does this violate any policies?: {user_message}"
    results = moderator_collection.query(query_texts=[query], n_results=10, include=["metadatas", "documents"])
    constantBias = [
        'My Name is The Moderator.',
        'I always respond within 10 words and try to be concise.',
        'I don\'t need to respond to every message.'
        'If the user message does not require moderation, you may reply with nothing or say "No response needed."'

    ]

    # Separate results by type
    policies = [doc for doc, meta in zip(results["documents"][0], results["metadatas"][0]) if "policy" in meta["type"]]
    biases = [doc for doc, meta in zip(results["documents"][0], results["metadatas"][0]) if "bias" in meta["type"]]
    jokes = [doc for doc, meta in zip(results["documents"][0], results["metadatas"][0]) if "joke" in meta["type"]]
    prompt = f"""
        You are a quirky, sometimes biased, sometimes funny chat moderator.
        Policy: {', '.join(policies) if policies else 'No relevant policy found.'}
        Bias: {', '.join(constantBias + biases) if biases else 'No relevant bias found.'}
        Joke: {', '.join(jokes) if jokes and random.random() < joke_chance else 'No relevant joke found.'}
        ConstantBias: My Name is The Moderator. I always respond within 10 words and try to be concise. I don't need to respond to every message.
        User message: {user_message}
        As the moderator, respond to the user, enforcing the policy, showing your bias, and optionally including the joke.
        """
    response = generate_chat_response(prompt)
    return response.strip()
