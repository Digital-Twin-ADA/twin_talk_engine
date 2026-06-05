import json
import os
import uuid
from datetime import datetime

from azure.cosmos import CosmosClient
from groq import Groq

from twin_talk_engine import AGENT_INSTRUCTION
from twin_talk_engine.repositories.cosmos_repository import CosmosRepository
from twin_talk_engine.services.context_builder import ContextBuilder
from twin_talk_engine.tools.schemas import TOOLS


class AIClient:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")

        self.repo = CosmosRepository()
        self.context_builder = ContextBuilder(self.repo)

    def _execute_tool_calls(self, tool_calls) -> list:
        from twin_talk_engine.tools.registry import TOOL_REGISTRY

        tool_messages = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            raw_args = tool_call.function.arguments
            tool_args = json.loads(raw_args) if raw_args else {}
            if tool_args is None:
                tool_args = {}

            tool_fn = TOOL_REGISTRY.get(tool_name)
            if not tool_fn:
                tool_result = {"error": f"Tool '{tool_name}' not found"}
            else:
                try:
                    tool_result = (
                        tool_fn(**tool_args)
                        if isinstance(tool_args, dict)
                        else tool_fn()
                    )
                except Exception as e:
                    tool_result = {"error": str(e)}

            tool_messages.append({"tool": tool_name, "data": tool_result})
        return tool_messages

    def _handle_tool_flow(
        self, session_id: str, user_name: str, groq_messages: list, tool_calls
    ) -> str:
        tool_messages = self._execute_tool_calls(tool_calls)

        second_response_messages = [
            {
                "role": "system",
                "content": AGENT_INSTRUCTION
                + "\n\nYou MUST answer ONLY using the provided tool data. Do NOT say you don't have data.",
            }
        ]
        second_response_messages.extend(groq_messages[1:])
        second_response_messages.append(
            {
                "role": "system",
                "content": f"TOOL DATA:\n{json.dumps(tool_messages, indent=2)}",
            }
        )

        second_response = self.client.chat.completions.create(
            messages=second_response_messages,
            model=self.model,
        )

        final_content = second_response.choices[0].message.content
        self.repo.save_message(session_id, user_name, "assistant", final_content)
        return final_content

    def chat(self, session_id: str, user_name: str, user_message: str) -> str:
        print("\n=== NEW REQUEST ===")
        print("USER:", user_message)

        groq_messages = self.context_builder.build_messages_context(
            session_id, user_message
        )
        self.repo.save_message(session_id, user_name, "user", user_message)

        response = self.client.chat.completions.create(
            messages=groq_messages,
            model=self.model,
            tools=TOOLS,
        )

        message = response.choices[0].message
        print("\n--- MODEL RESPONSE ---")
        print("CONTENT:", message.content)
        print("TOOL CALLS:", message.tool_calls)

        if message.tool_calls:
            return self._handle_tool_flow(
                session_id, user_name, groq_messages, message.tool_calls
            )

        print("\n--- NO TOOL USED ---")
        self.repo.save_message(session_id, user_name, "assistant", message.content)
        return message.content

    def get_welcome_message(self, session_id: str, user_name: str) -> str:
        welcome_text = (
            f"Hello {user_name}! I am your Digital Twin Assistant for the festival. "
            "How can I help you tonight? I can check the artist lineups, look up ongoing events, "
            "and help you navigate everything happening around the venue!"
        )

        self.repo.save_message(session_id, user_name, "assistant", welcome_text)

        return welcome_text
