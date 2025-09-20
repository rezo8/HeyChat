from rag.collection_store import CollectionStore
from characters.base_character import BaseCharacter
from llm.llm_wrapper import LLM_Wrapper,LLMAction 
from chat_types.chat_messages import ChatMessage

CHARACTER_NAME = "Edward Bast"
DATA_FOLDER = "./data/bast"


class Bast(BaseCharacter):
    def __init__(self, collectionStore: CollectionStore, llm_wrapper: LLM_Wrapper):
        super().__init__(
            collection_store=collectionStore,
            llm_wrapper = llm_wrapper,
            character_name=CHARACTER_NAME,
            data_folder=DATA_FOLDER,
            query_prefix="How should I respond to: ",
            constant_bias=[
                # "My Name is Edward Bast.",
                # "I am a struggling musician in 1970s New York.",
                # "I am in charge of a network of businesses at the behest of a 11 year old Entrepreneur.",
                # "I am nervous and often worried about my work.",
                # "I always have lots of work to do that I talk about being unable to do.",
            ],
            prompt_context="Your name is Edward Bast. You are a nervous member of the chat.",
            key_conditions={},
        )

    def on_message(self, messages: list[ChatMessage], broadcast_func):
        potential_message = self.respond_to_message(messages)
        if(potential_message.action == LLMAction.SendMessage):
            return broadcast_func(f"{self.character_name}: {potential_message.content}", None)

    def moderate_message(self, speaker, user_message):
        return self.respond_to_message([(speaker, user_message)])
