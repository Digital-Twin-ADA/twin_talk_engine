import os
import uuid
from datetime import datetime

from azure.cosmos import CosmosClient


class CosmosRepository:
    def __init__(self):
        connection_string = os.getenv("COSMOS_CONNECTION_STRING")
        if not connection_string:
            raise ValueError(
                "COSMOS_CONNECTION_STRING is not set in environment variables"
            )

        self.client = CosmosClient.from_connection_string(connection_string)
        self.db = self.client.get_database_client("twintalk-db")
        self.container = self.db.get_container_client("chat-history")

    def save_message(
        self, session_id: str, user_name: str, role: str, content: str
    ) -> None:
        try:
            document = {
                "id": str(uuid.uuid4()),
                "sessionId": session_id,
                "userName": user_name,
                "role": role,
                "content": content,
                "createdAt": datetime.utcnow().isoformat(),
            }
            self.container.create_item(body=document)
        except Exception as e:
            print(f"[CosmosRepository Error on Save]: {e}")

    def get_raw_history(self, session_id: str) -> list:
        try:
            query = (
                "SELECT c.role, c.content "
                "FROM c "
                "WHERE c.sessionId = @sessionId "
                "ORDER BY c.createdAt ASC"
            )
            parameters = [{"name": "@sessionId", "value": session_id}]

            items = list(
                self.container.query_items(
                    query=query,
                    parameters=parameters,
                    enable_cross_partition_query=False,
                )
            )
            return items
        except Exception as e:
            print(f"[CosmosRepository Error on Read]: {e}")
            return []
