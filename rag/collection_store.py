import chromadb
import os
import hashlib


class CollectionStore:
    client = chromadb.PersistentClient(f"./.chromadb")
    collection: chromadb.Collection

    def __init__(
        self,
        collection_name,
    ):
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def trainCollection(self, metadata: list[dict], dataFolderPath: str) -> list[str]:
        relevantKeys = []
        for filename in os.listdir(dataFolderPath):
            if filename.endswith(".txt"):
                fileNamePrefix = filename[:-4]
                relevantKeys.append(fileNamePrefix)
                with open(os.path.join(dataFolderPath, filename), "r") as f:
                    policies: list[str] = f.read().splitlines()
                    ids = [self.__get_line_hash(policy) for policy in policies]
                    self.collection.add(
                        ids=ids,
                        documents=policies,
                        metadatas=[
                            {**{"line": lineNum, "type": fileNamePrefix}, **metadata}
                            for lineNum in range(len(policies))
                        ],
                    )

        return relevantKeys

    def __get_line_hash(self, line: str) -> str:
        clean = line.strip()[:56]  # Remove leading/trailing whitespace, then take first 56 chars 
        return hashlib.sha256(clean.encode("utf-8")).hexdigest()
