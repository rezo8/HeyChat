import os
import chromadb
import hashlib


def build_character(name: str, description: str, dataFolderPath: str):
    client = chromadb.PersistentClient(f"{dataFolderPath}/.chromadb")

    collection = client.get_or_create_collection(name="training_info")
    # Open all files in dataFolderPath and add them to the collection
    for filename in os.listdir(dataFolderPath):
        if filename.endswith(".txt"):
            fileNamePrefix = filename[:-4]
            with open(os.path.join(dataFolderPath, filename), "r") as f:
                policies: list[str] = f.read().splitlines()
                ids = [__get_line_hash(policy) for policy in policies]
                collection.add(
                    ids=ids,
                    documents=policies,
                    metadatas=[
                        {
                            "line": lineNum,
                            "type": fileNamePrefix,
                            "character": name,
                            "description": description,
                        }
                        for lineNum in range(len(policies))
                    ],
                )
    return collection


def __get_line_hash(line: str) -> str:
    clean = line.strip()[
        :56
    ]  # Remove leading/trailing whitespace, then take first 56 chars
    return hashlib.sha256(clean.encode("utf-8")).hexdigest()
