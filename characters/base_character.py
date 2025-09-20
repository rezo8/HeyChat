import chromadb
import random
from rag.collection_store import CollectionStore
from collections import deque
from llm.llm_wrapper import LLM_Wrapper
from chat_types.chat_messages import ChatMessage
from chat_types.llm_response import LLMResponse
from abc import ABC, abstractmethod


class BaseCharacter(ABC):
    collection_store: CollectionStore
    llm_wrapper: LLM_Wrapper
    character_name: str
    character_keys: list[str]
    query_prefix: (
        str  # How we frame the query to chromadb TODO make this in DataFolder somehow
    )
    constant_bias: list[str]
    prompt_context: str  # How do we make sure chromaDB always adds this so we can leverage data folder.
    prompt_signoff: str  # How we signoff the query to chromaDB : TODO make this in DataFolder somehow
    key_conditions: dict[str, float]
    response_history: deque

    def __init__(
        self,
        collection_store: CollectionStore,
        llm_wrapper: LLM_Wrapper,
        character_name: str,
        data_folder: str,
        query_prefix: str,
        constant_bias: list[str],
        prompt_context: str,
        key_conditions: dict[str, float] = {},
        history_size: int = 10,  # configurable size
    ):

        self.collection_store = collection_store
        self.llm_wrapper = llm_wrapper
        self.character_name = character_name
        self.constant_bias = constant_bias
        self.query_prefix = query_prefix
        self.prompt_context = prompt_context
        self.key_conditions = key_conditions
        self.response_history = deque(maxlen=history_size)
        character_keys = self.collection_store.trainCollection(
            {"character": self.character_name}, data_folder
        )
        self.character_keys = character_keys

    @abstractmethod
    def on_message(self, messages: list[ChatMessage], broadcast_func):
        pass  #

    def respond_to_message(
        self,
        relevant_messages: list[ChatMessage],  # How will it handle more than 1 message?
        n_results=5,
    ) -> LLMResponse:
        # TODO remove query_prefix.
        print(relevant_messages)
        query_string = f"".join(
            [msg.format_for_query() for msg in relevant_messages]
        )
        # I need to improve the customization coming from Chroma.
        chroma_response = self.collection_store.collection.query(
            query_texts=[query_string],
            n_results=n_results,
            include=["metadatas", "documents"],
            where={"character": self.character_name},
        )
        personalityInfo = self.__generatePersonalityInfo(chroma_response)
        print(personalityInfo)
        messagesToRespondTo = self.__generateMessagesToRespondTo(relevant_messages)
        response: LLMResponse = self.llm_wrapper.generate_chat_response(personalityInfo, messagesToRespondTo)
        self.response_history.append(response.content)
        # TODO handle the response actions.
        return response

    def __generatePersonalityInfo(self, queryResult: chromadb.QueryResult):
        responseByType: dict[str, list[str]] = {}


        for doc, meta in zip(queryResult["documents"][0], queryResult["metadatas"][0]):
            current: list[str] = responseByType.get(meta["type"], [])
            current.append(doc)
            responseByType[meta["type"]] = current
        print('resoonseByType before adding constant bias', responseByType)
        return responseByType
    
    def __generateMessagesToRespondTo(self, userMessages: list[ChatMessage]):
        return [msg.format_for_query() for msg in userMessages]

    # TODO split this from response information and then messages to respond to in LLM Wrapper
    # def __generatePrompt(
    #     self, userMessages: list[ChatMessage], queryResult: chromadb.QueryResult
    # ): 
    #     print('generating prompt')
    #     print('userMessages', userMessages)
    #     responseByType: dict[str, list[str]] = {}
    #     responseByType["ConstantBias"] = self.constant_bias
    #     responseByType["Messages to Respond to"] = [msg.format_for_query() for msg in userMessages]
    #     # TODO Don't be limited to first document.
    #     relevant_docs = zip(queryResult["documents"][0], queryResult["metadatas"][0])
    #     for doc, meta in relevant_docs:
    #         for type in meta["type"]:
    #             current: list[str] = responseByType.get(type, [])
    #             current.append(doc)
    #             responseByType[type] = current

    #     prompt = self.prompt_context + "\n"
    #     for x, y in responseByType.items():
    #         apply = (
    #             random.random() < self.key_conditions[x]
    #             if x in self.key_conditions
    #             else True
    #         )
    #         if apply:
    #             prompt += f"{x}: {', '.join(y)}\n"
    #     return prompt
