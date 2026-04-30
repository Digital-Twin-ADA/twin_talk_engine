import json
import os

from groq import Groq

from twin_talk_engine import AGENT_INSTRUCTION
from twin_talk_engine.tools.schemas import TOOLS


class AIClient:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")

    def chat(self, user_message: str) -> str:
        print("\n=== NEW REQUEST ===")
        print("USER:", user_message)

        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": AGENT_INSTRUCTION},
                {"role": "user", "content": user_message},
            ],
            model=self.model,
            tools=TOOLS,
        )

        message = response.choices[0].message

        print("\n--- MODEL RESPONSE ---")
        print("CONTENT:", message.content)
        print("TOOL CALLS:", message.tool_calls)

        if message.tool_calls:
            from twin_talk_engine.tools.registry import TOOL_REGISTRY

            tool_messages = []

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name

                raw_args = tool_call.function.arguments
                tool_args = json.loads(raw_args) if raw_args else {}

                if tool_args is None:
                    tool_args = {}

                print("\n--- TOOL CALL ---")
                print("NAME:", tool_name)
                print("RAW ARGS:", raw_args)
                print("PARSED ARGS:", tool_args)

                tool_fn = TOOL_REGISTRY.get(tool_name)

                if not tool_fn:
                    tool_result = {"error": f"Tool '{tool_name}' not found"}
                else:
                    try:
                        if isinstance(tool_args, dict):
                            tool_result = tool_fn(**tool_args)
                        else:
                            tool_result = tool_fn()
                    except Exception as e:
                        tool_result = {"error": str(e)}

                print("RESULT:", tool_result)

                tool_messages.append({"tool": tool_name, "data": tool_result})

            second_response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": AGENT_INSTRUCTION
                        + "\n\nYou MUST answer ONLY using the provided tool data. Do NOT say you don't have data.",
                    },
                    {"role": "user", "content": user_message},
                    {
                        "role": "system",
                        "content": f"TOOL DATA:\n{json.dumps(tool_messages, indent=2)}",
                    },
                ],
                model=self.model,
            )

            print("\n--- FINAL RESPONSE ---")
            print(second_response.choices[0].message.content)

            return second_response.choices[0].message.content

        print("\n--- NO TOOL USED ---")
        return message.content
