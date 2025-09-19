from characters.moderator import Moderator
from rag.collection_store import CollectionStore


collectionStore = CollectionStore("characters")
moderator = Moderator(collectionStore)


def main():
    speaker = "User"
    user_message = "This is a test message that might violate policies."
    response = moderator.moderate_message(speaker, user_message)
    print(f"Moderator Response: {response}")


if __name__ == "__main__":
    main()
