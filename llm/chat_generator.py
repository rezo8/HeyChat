import ollama


def generate_chat_response(prompt, model="llama3") -> str:
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]
