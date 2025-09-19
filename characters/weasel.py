from rag.collection_store import CollectionStore
from characters.base_character import BaseCharacter

CHARACTER_NAME = "Vinnie the Weasel"
DATA_FOLDER = "./data/theWeasel"



class VinnieTheWeasel(BaseCharacter):
    def __init__(self, collectionStore: CollectionStore):
        super().__init__(
            collection_store=collectionStore,
            character_name=CHARACTER_NAME,
            data_folder=DATA_FOLDER,
            query_prefix="How should I respond to: ",
                constant_bias=[
                    "My name is Vinnie, but everyone calls me The Weasel.",
                    "I'm always looking for the next big score or a quick hustle.",
                    "I never trust anyone completely—someone’s always watching."
                ],
            prompt_context="Your name is Vinnie the Weasel. You are a cunning and street-smart character.",
            prompt_signoff="" \
            "Respond to the user." \
            "Determine if you want to respond or not. If you respond, finish statement with \"Send Response.\" If you do not want to respond, finish with \"No Response.\" DO NOT OMIT THE PERIODS",
            key_conditions={},
        )

    def on_message(self, message, broadcast_func):
        potential_message = self.respond_to_message([f"User: {m}" for m in message])
        print(potential_message)
        if potential_message.endswith("Send Response."):
            potential_message = potential_message[:-len("Send Response.")].strip()
            return broadcast_func(f"{self.character_name}: {potential_message}", None)

    def moderate_message(self, speaker, user_message):
        return self.respond_to_message([(speaker, user_message)])
