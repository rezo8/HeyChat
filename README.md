## Usage

1. Start Ollama and ensure your desired model (e.g., llama3) is running.
2. Run your main chatroom script:
  ```sh
  python main.py
  ```
3. The chatroom will use ChromaDB for retrieval and Ollama for generating AI character responses.

You can modify or extend the personalities and data in the `/data` directory, and adjust the logic in the `/characters` and `/llm` modules as needed.
# HeyChat
A Repo that runs a ChatRoom with different AI personalities

## Dependencies

- [ChromaDB](https://www.trychroma.com/)  
  For vector storage and retrieval (RAG).

- [Ollama](https://ollama.com/)  
  For running local LLMs and generating chat responses.

## Installation

1. Install Python dependencies:
  ```sh
  pip install chromadb sentence-transformers ollama
  ```

2. Install Ollama (for local LLMs):
  [Download Ollama](https://ollama.com/download) and follow the instructions for your OS.

3. Pull a model (e.g., llama3) for Ollama:
  ```sh
  ollama pull llama3
  ```

4. Run the project as described in the usage section.
