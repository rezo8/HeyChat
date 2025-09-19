import chromadb
import random
from rag.collection_store import CollectionStore
from collections import deque
from llm.chat_generator import generate_chat_response
from abc import ABC, abstractmethod


class BaseCharacter(ABC):
    collection_store: CollectionStore
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
        character_name: str,
        data_folder: str,
        query_prefix: str,
        constant_bias: list[str],
        prompt_context: str,
        prompt_signoff: str,
        key_conditions: dict[str, float] = {},
        history_size: int = 10,  # configurable size
    ):
        character_keys = collection_store.trainCollection(
            {"character": character_name}, data_folder
        )

        self.collection_store = collection_store
        self.character_name = character_name
        self.character_keys = character_keys
        self.constant_bias = constant_bias
        self.query_prefix = query_prefix
        self.prompt_context = prompt_context
        self.prompt_signoff = prompt_signoff
        self.key_conditions = key_conditions
        self.response_history = deque(maxlen=history_size)

    @abstractmethod
    def on_message(self, message, broadcast_func):
        pass  # 

    def respond_to_message(
        self,
        relevant_messages: list[(str, str)],  # How will it handle more than 1 message?
        n_results=10,
    ):
        query_string = f"{self.query_prefix}\n".join(
            [f"{speaker}: {content}" for speaker, content in relevant_messages]
        )
        
        chroma_response = self.collection_store.collection.query(
            query_texts= [query_string],
            n_results=n_results,
            include=["metadatas", "documents"],
            where={"name": self.character_name},
        )

        prompt = self.__generatePrompt(relevant_messages, chroma_response)
        response = generate_chat_response(prompt).strip()
        self.response_history.append(response)
        return response

    def __generatePrompt(
        self, userMessages: list[(str, str)], queryResult: chromadb.QueryResult
    ):
        responseByType: dict[str, list[str]] = {}
        responseByType["ConstantBias"] = self.constant_bias
        responseByType["Messages to Respond to"] = [f"{speaker} Says: {content}" for speaker, content in userMessages]
        # TODO Don't be limited to first document.
        relevant_docs = zip(queryResult["documents"][0], queryResult["metadatas"][0])
        for doc, meta in relevant_docs:
            for type in meta["type"]:
                current: list[str] = responseByType.get(type, [])
                current.append(doc)
                responseByType.update(type, current)

        prompt = self.prompt_context + "\n"
        for x, y in responseByType.items():
            apply = (
                random.random() < self.key_conditions[x]
                if x in self.key_conditions
                else True
            )
            if apply:
                prompt += f"{x}: {', '.join(y)}\n"

        prompt += self.prompt_signoff
        return prompt
