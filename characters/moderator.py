import random

from rag.vector_store import build_character

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

    # Separate results by type
    policies = [doc for doc, meta in zip(results["documents"][0], results["metadatas"][0]) if "policy" in meta["type"]]
    biases = [doc for doc, meta in zip(results["documents"][0], results["metadatas"][0]) if "bias" in meta["type"]]
    jokes = [doc for doc, meta in zip(results["documents"][0], results["metadatas"][0]) if "joke" in meta["type"]]

    response = ""
    if policies:
        response += f"Policy: {policies[0]}\n"
    if biases:
        response += f"Moderator's bias: {random.choice(biases)}\n"
    if jokes and random.random() < joke_chance:
        response += f"Moderator's joke: {random.choice(jokes)}"
    return response.strip()
