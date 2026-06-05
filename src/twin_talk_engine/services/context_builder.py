from twin_talk_engine import AGENT_INSTRUCTION
from twin_talk_engine.repositories.cosmos_repository import CosmosRepository


class ContextBuilder:
    def __init__(self, repository: CosmosRepository):
        self.repository = repository

    def build_messages_context(
        self, session_id: str, current_user_message: str, limit: int = 10
    ) -> list:
        messages = [{"role": "system", "content": AGENT_INSTRUCTION}]

        raw_history = self.repository.get_raw_history(session_id)

        recent_history = raw_history[-limit:] if raw_history else []

        for msg in recent_history:
            messages.append({"role": msg["role"], "content": msg["content"]})

        messages.append({"role": "user", "content": current_user_message})

        return messages
