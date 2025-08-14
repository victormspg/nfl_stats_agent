import random
import psycopg2
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
            print(f"Messages stored in PostgreSQL for session: {self.session_id}")
        except Exception as e:
            print(f"Error storing messages in PostgreSQL: {e}")
            self.conn.rollback()
            raise

    async def read_history(self):
        """Read the chat history from PostgreSQL."""
        try:
            self.cur.execute(
                "SELECT messages FROM user_chats WHERE session_id = %s AND customer_id = %s",
                (self.session_id, str(self.customer_id))
            )
            row = self.cur.fetchone()
            if not row:
                print("No chat history for this customer and session_id was retrieved.")
                return False
            messages = row[0]
            for m in messages:
                await self.on_new_message(ChatMessageContent.model_validate(m))
            print("Messages were retrieved from PostgreSQL")
            return True
        except Exception as e:
            print(f"Error reading messages from PostgreSQL: {e}")
            return False
    

async def start_chat(support_agent, db_chat_history_uri):
    """Starts the chat with the support agent."""
    print("Welcome to Football Stats Agent Chat!")
    print("You can ask questions about games, players, and statistics.")
    print("Type 'exit' to end the chat.")
    customer_id = input("Please enter your customer ID: ")
    session_id = input("Please enter your session ID (or press Enter if this is a new chat/topic): ")

    # initate chat_history_db connection
 
    if not db_chat_history_uri:
        print("Failed to retrieve chat history database URI.")
        return False
    chat_history_conn = psycopg2.connect(db_chat_history_uri)
    chat_cur = chat_history_conn.cursor()

    # initiate chat history object
    hist = ChatHistoryInPostgresDB(
            session_id=session_id,
            customer_id=customer_id,
            conn=chat_history_conn,
            cur=chat_cur
        )
    res = await hist.read_history()

    if(not res):
        print("No previous chat history found for this customer. Starting a new chat session...")
        session_id = f"session_"+random.randint(1000, 9999).__str__()
        hist = ChatHistoryInPostgresDB(
            session_id=session_id,
            customer_id=customer_id,
            conn=chat_history_conn,
            cur=chat_cur
        )
        print(f"Customer ID: {hist.customer_id}, Session ID: {hist.session_id}\n")

    while True:
        raw_input = input("How can I help you today? (Type 'exit' to end the chat) > ") if hist.session_id == session_id else input("Customer > ")
        if raw_input.strip().lower() == "exit":
            await hist.store_history()
            print("NOTE: If you would like to continue this chat in the future, use this session ID:", session_id)
            break
        user_input = f"Customer ID {customer_id}: {raw_input}"
        print(user_input)
        response = await support_agent.get_response(messages=user_input, thread=hist)
        print(f"Support Agent: {response}")
    return True