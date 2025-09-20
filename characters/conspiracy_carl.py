from rag.collection_store import CollectionStore
from characters.base_character import BaseCharacter
from llm.llm_wrapper import LLM_Wrapper

CHARACTER_NAME = "Conspiracy Carl"
DATA_FOLDER = "./data/conspiracyCarl"


class ConspiracyCarl(BaseCharacter):
    def __init__(self, collectionStore: CollectionStore, llm_wrapper: LLM_Wrapper):
        super().__init__(
            collection_store=collectionStore,
            llm_wrapper = llm_wrapper,
            character_name=CHARACTER_NAME,
            data_folder=DATA_FOLDER,
            query_prefix="How should I respond to: ",
            constant_bias=[
                "My name is Carl, but everyone calls me Conspiracy Carl.",
                "I see hidden plots and secret agendas everywhere.",
                "I never take anything at face value—there’s always more beneath the surface.",
            ],
            prompt_context="Your name is Conspiracy Carl. You are a suspicious, theory-loving member of the chat.",
            key_conditions={},
        )

    def on_message(self, message, broadcast_func):
        potential_message = self.respond_to_message([f"User: {m}" for m in message])
        if potential_message.endswith("Send Response."):
            potential_message = potential_message.removesuffix("Send Response.").strip()
            return broadcast_func(f"{self.character_name}: {potential_message}", None)
        return None

    def moderate_message(self, speaker, user_message):
        return self.respond_to_message([(speaker, user_message)])
