from dataclasses import dataclass
from typing import Optional, Dict, Literal

from enum import Enum

class LLMAction(Enum):
    SendMessage = "SendMessage"
    BlockMessage = "BlockMessage"
    AllowMessage = "AllowMessage"
    StayQuiet = "StayQuiet"

ModeratorActions = [LLMAction.BlockMessage, LLMAction.AllowMessage]
ChatBotActions = [LLMAction.SendMessage, LLMAction.StayQuiet]

@dataclass
class LLMResponse:
    sender: str
    role: str
    content: str
    type: Optional[str] = "chat"
    action: Optional[LLMAction] = None
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
