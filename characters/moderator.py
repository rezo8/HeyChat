from rag.collection_store import CollectionStore
from characters.base_character import BaseCharacter
from llm.llm_wrapper import LLM_Wrapper

CHARACTER_NAME = "Moderator"
DATA_FOLDER = "./data/moderator"


## TODO it should have a conditional broadcast/be a filter for messages before they are broadcasted maybe?
class Moderator(BaseCharacter):
    # TODO make not so noisy. it really shouldn't be dominating conversation.
    def __init__(self, collectionStore: CollectionStore, llm_wrapper: LLM_Wrapper):
        super().__init__(
            collection_store=collectionStore,
            llm_wrapper = llm_wrapper,
            character_name=CHARACTER_NAME,
            data_folder=DATA_FOLDER,
            query_prefix="Do these messages violate any policies?: ",
            constant_bias=[
                "My Name is The Moderator.",
                "I always respond within 10 words and try to be concise.",
                "I don't need to respond to every message.",
                'If the user message does not require moderation, you may reply with nothing or say "No response needed."',
            ],
            prompt_context="Your name is the Moderator. You are a quirky, sometimes biased, sometimes funny chat moderator.",
            key_conditions={"joke": 0.4},
        )

    def on_message(self, message, broadcast_func):
        potential_message = self.respond_to_message([("User", message)])
        print(potential_message)
        return broadcast_func(f"{self.character_name}: {potential_message}", None)
