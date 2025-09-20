from dataclasses import dataclass

@dataclass
class ChatMessage:
    sender: str
    role: str
    content: str
    type: str = "chat"

    def format_for_query(self) -> str:
            """Format this message for LLM prompt input."""
            return f"{self.sender} ({self.role}): {self.content}"
