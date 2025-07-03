# nodes/state.py
from typing import List, Dict, Optional, Any
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field

class AgentState(BaseModel):
    user_input: str
    chat_history: List[BaseMessage] = Field(default_factory=list)
    slots: Dict[str, Any] = Field(default_factory=dict)
    final_answer: Optional[str] = None
    tool_calls: List[Any] = Field(default_factory=list)
    all_required_slots_filled: bool = False
