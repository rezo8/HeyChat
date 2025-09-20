import ollama
import json
from chat_types.llm_response import LLMAction, LLMResponse, ChatBotActions, ModeratorActions

class LLM_Wrapper:
    MAX_HISTORY = 10
    model: str
    messages: list[dict[str, str]]
    def __init__(self, model="llama3"):
        self.model = model
        action_values = "|".join([a.value for a in LLMAction])
        self.messages = [{
            "role": "system",
            "content": (
                "You are a chat participant in a multi-user chatroom. "
                "Always return your responses in the following JSON format. Make sure all values are JSON Valid:\n"
                "{\n"
                '  "sender": \"<your name>\",\n'
                '  "role": \"<role>\",\n'
                '  "content": \"<your message>\",\n'
                '  "type": \"<chat|moderation|system>\",\n'
                f'  "action": \"This must exist and be one of the following values <{action_values}>\",\n'
                '  "timestamp": \"<ISO8601 timestamp>\",\n'
                '  "metadata": { ... }\n'
                "}\n"
                f"For non-moderator bots, always include one of {[a.value for a in ChatBotActions]} in the action field."
                f"For moderators, always include one of {[a.value for a in ModeratorActions]} in the action field."
                "YOU MUST HAVE A VALID ACTION IN YOUR RESPONSE."
                "Respond only in this JSON format—do not include any extra text or explanation."
            )
        }]

        return

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def generate_chat_response(self, prompt: str, model="llama3") -> LLMResponse:
        toSend = prompt + self.messages
        print('toSend', toSend)
        response = ollama.chat(model=model, messages=toSend)
        message = parse_llm_content(response.message.content)
        print('message', message)
        llm_response = LLMResponse(
            sender=message.get("sender", "Unknown"),
            role=message.get("role", "bot"),
            content=message.get("content", ""),
            type=message.get("type", "chat"),
            action=LLMAction(message.get("action", "StayQuiet")),
            timestamp=message.get("timestamp"),
            metadata=message.get("metadata", {})
        )
        print('llm response', llm_response)
        return llm_response

def parse_llm_content(content: str) -> dict:
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Failed to parse LLM content as JSON: {e}")
        return {}
