from pydantic import BaseModel, field_validator
from typing import Optional, Union, List, Dict, Any, Literal


class BaseMessage(BaseModel):
    content: str = ""

    # The OpenAI API returns content=None when the model only makes tool calls
    @field_validator("content", mode="before")
    @classmethod
    def _none_to_empty(cls, value: Any) -> Any:
        return "" if value is None else value

    def dict(self, **kwargs: Any) -> Dict[str, Any]:
        return dict(self)


class SystemMessage(BaseMessage):
    role: Literal["system"] = "system"


class UserMessage(BaseMessage):
    role: Literal["user"] = "user"


class ToolMessage(BaseMessage):
    role: Literal["tool"] = "tool"
    tool_call_id: str
    name: str


class AIMessage(BaseMessage):
    role: Literal["assistant"] = "assistant"
    tool_calls: Optional[List[Any]] = None


AnyMessage = Union[
    SystemMessage,
    UserMessage,
    AIMessage,
    ToolMessage,
]
