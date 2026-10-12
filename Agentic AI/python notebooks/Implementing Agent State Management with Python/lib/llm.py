from typing import List, Optional, Dict, Any, Sequence, Type
from pydantic import BaseModel
from openai import OpenAI
from lib.messages import (
    AIMessage,
    BaseMessage,
    UserMessage,
)
from lib.tooling import Tool, ToolCall
import os

class LLM:
    def __init__(
        self,
        model: str = "gpt-4o-mini",
        temperature: float = 0.0,
        tools: Optional[List[Tool]] = None,
        api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    ):
        self.model = model
        self.temperature = temperature
        self.client = OpenAI(api_key=api_key) if api_key else OpenAI()
        self.tools: Dict[str, Tool] = {
            tool.name: tool for tool in (tools or [])
        }

    def register_tool(self, tool: Tool):
        self.tools[tool.name] = tool

    def _build_payload(self, messages: List[BaseMessage]) -> Dict[str, Any]:
        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "messages": [m.dict() for m in messages],
        }

        if self.tools:
            payload["tools"] = [tool.dict() for tool in self.tools.values()]
            payload["tool_choice"] = "auto"

        return payload

    def _convert_input(self, input: Any) -> List[BaseMessage]:
        if isinstance(input, str):
            return [UserMessage(content=input)]
        elif isinstance(input, BaseMessage):
            return [input]
        elif isinstance(input, list) and all(isinstance(m, BaseMessage) for m in input):
            return list(input)
        else:
            raise ValueError(f"Invalid input type {type(input)}.")

    def invoke(self, 
               # Sequence (not List) so a list of any BaseMessage subclasses is accepted
               input: str | BaseMessage | Sequence[BaseMessage],
               response_format: Optional[Type[BaseModel]] = None,) -> AIMessage:
        messages = self._convert_input(input)
        payload = self._build_payload(messages)
        if response_format:
            payload.update({"response_format": response_format})
            response = self.client.beta.chat.completions.parse(**payload)
        else:
            response = self.client.chat.completions.create(**payload)
        choice = response.choices[0]
        message = choice.message

        # .parse() returns a list of a ToolCall subclass; copy it into a List[ToolCall]
        tool_calls: Optional[List[ToolCall]] = (
            [*message.tool_calls] if message.tool_calls is not None else None
        )
        return AIMessage(
            content=message.content or "",
            tool_calls=tool_calls
        )
