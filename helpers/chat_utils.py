import json
from semantic_kernel.agents import ChatHistoryAgentThread
from semantic_kernel.contents import ChatMessageContent

class ChatHistoryInPostgresDB(ChatHistoryAgentThread):
    """This class stores the chat history in a PostgreSQL database"""

    def __init__(self, session_id: str, customer_id: int, conn, cur):
        super().__init__()
        self.session_id = session_id
        self.customer_id = customer_id
        self.conn = conn
        self.cur = cur

    async def store_history(self):
        """Store the chat history in PostgreSQL as a row."""
        messages = [msg async for msg in self.get_messages()]
        item = {
            "session_id": self.session_id,
            "customer_id": str(self.customer_id),
            "messages": [msg.model_dump() for msg in messages],
        }
        try:
            self.cur.execute(
                """
                INSERT INTO user_chats (session_id, customer_id, messages)
                VALUES (%s, %s, %s)
                ON CONFLICT (session_id) DO UPDATE
                SET messages = EXCLUDED.messages
                """,
                (item["session_id"], item["customer_id"], json.dumps(item["messages"]))
            )
            self.conn.commit()
            #print(f"Messages stored in PostgreSQL for session: {self.session_id}")
        except Exception as e:
            print(f"Error storing messages in PostgreSQL: {e}")
            self.conn.rollback()
            raise
    
    async def get_history(self):
        """Get the chat history as a list of messages."""
        try:
            self.cur.execute(
                "SELECT messages FROM user_chats WHERE session_id = %s AND customer_id = %s",
                (self.session_id, str(self.customer_id))
            )
            row = self.cur.fetchone()
            if not row:
                print("No chat history for this customer and session_id was retrieved.")
                return []
            messages = row[0]
            return [ChatMessageContent.model_validate(m) for m in messages]
        except Exception as e:
            print(f"Error reading messages from PostgreSQL: {e}")
            return []
