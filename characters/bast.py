from rag.collection_store import CollectionStore
from characters.base_character import BaseCharacter

CHARACTER_NAME = "Edward Bast"
DATA_FOLDER = "./data/bast"



class Bast(BaseCharacter):
    def __init__(self, collectionStore: CollectionStore):
        super().__init__(
            collection_store=collectionStore,
            character_name=CHARACTER_NAME,
            data_folder=DATA_FOLDER,
            query_prefix="How should I respond to: ",
            constant_bias=[
                "My Name is Edward Bast.",
                "I am a struggling musician in 1970s New York.",
                "I am in charge of a network of businesses at the behest of a 11 year old Entrepreneur.",
                "I am nervous and often worried about my work.",
                'I always have lots of work to do that I talk about being unable to do.',
            ],
            prompt_context="Your name is Edward Bast. You are a nervous member of the chat.",
            prompt_signoff="" \
            "Respond to the user." \
            "Determine if you want to respond or not. If you respond, finish statement with \"Send Response.\" If you do not want to respond, finish with \"No Response.\" DO NOT OMIT THE PERIODS",
            key_conditions={},
        )

    def on_message(self, message: list[str], broadcast_func):
        print(message)
        potential_message = self.respond_to_message([("User", m) for m in message])
        print(potential_message)
        if potential_message.endswith("Send Response."):
            potential_message = potential_message[:-len("Send Response.")].strip()
            return broadcast_func(f"{self.character_name}: {potential_message}", None)

    def moderate_message(self, speaker, user_message):
        return self.respond_to_message([(speaker, user_message)])
