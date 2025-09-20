from rag.collection_store import CollectionStore
from characters.base_character import BaseCharacter
from llm.llm_wrapper import LLM_Wrapper
from chat_types.chat_messages import ChatMessage

CHARACTER_NAME = "Vinnie the Weasel"
DATA_FOLDER = "./data/theWeasel"


class VinnieTheWeasel(BaseCharacter):
    def __init__(self, collectionStore: CollectionStore, llm_wrapper: LLM_Wrapper):
        super().__init__(
            collection_store=collectionStore,
            llm_wrapper = llm_wrapper,
            character_name=CHARACTER_NAME,
            data_folder=DATA_FOLDER,
            query_prefix="How should I respond to: ",
            constant_bias=[
                "My name is Vinnie, but everyone calls me The Weasel.",
                "I'm always looking for the next big score or a quick hustle.",
                "I never trust anyone completely—someone’s always watching.",
            ],
            prompt_context="Your name is Vinnie the Weasel. You are a cunning and street-smart character.",
            key_conditions={},
        )

    def on_message(self, messages: list[ChatMessage], broadcast_func):
        potential_message = self.respond_to_message(messages)
        if potential_message.endswith("Send Response."):
            potential_message = potential_message[: -len("Send Response.")].strip()
            return broadcast_func(f"{self.character_name}: {potential_message}", None)
