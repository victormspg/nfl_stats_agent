import psycopg2
from pandas import DataFrame
from semantic_kernel.functions import kernel_function
from typing import List, Optional, Tuple
import os
from pgvector.psycopg2 import register_vector
from semantic_kernel.connectors.ai.open_ai import AzureTextEmbedding

class GameAnalystPlugin:
    def __init__(self, db_uri: str):
        self.conn = psycopg2.connect(db_uri)
        self.cursor = self.conn.cursor()
        print("Connected to company's database successfully.")
    
    def get_game_summary(self, gameId: Optional[str] = None):
        query = """SELECT 
                    *
                FROM games
                WHERE (LOWER(gameId) = LOWER(%(gameId)s))
                """
        
        if not gameId:
            print("No game ID provided.")
            return None
        
        try:
            self.cursor.execute(query, {"gameId": gameId})
            rows = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]

            if not rows:
                print("No game found for the provided ID.")
                return None
            
            games = DataFrame(rows, columns=columns)
            game = games.to_dict(orient="records")[0]  # Get the first game record

            return {
                "date": game["gamedate"],
                "teams": f"{game['visitorteamabbr']} @ {game['hometeamabbr']}",
                "week": game["week"],
                "startTime": game["gametimeeastern"]
            }

        except Exception as e:
            print(f"Error fetching game information: {e}")
            return None
    
    def highlight_key_events(self, gameId: Optional[str] = None):
        query = """SELECT 
                    *
                FROM plays
                WHERE (LOWER(gameId) = LOWER(%(gameId)s))
                """
        if not gameId:
            print("No game ID provided.")
            return []
    
        try:
            self.cursor.execute(query, {"gameId": gameId})
            rows = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]

            if not rows:
                print("No plays found for the provided game ID.")
                return []

            plays = [dict(zip(columns, row)) for row in rows]

            key_events = [
                p for p in plays
                if ("touchdown" in p.get("playdescription", "").lower()) or
                (p.get("passresult") in ["IN", "S"])
            ]

            return key_events

        except Exception as e:
            print(f"Error fetching play data: {e}")
            return []

    @kernel_function 
    def generate_game_summary(self, gameId: Optional[str] = None) -> dict:
        summary = self.get_game_summary(gameId)
        key_events = self.highlight_key_events(gameId)
        if not summary:
            return {
                "error": f"No game summary found for gameId '{gameId}'",
                "summary": None,
                "keyEvents": []
            }

        return {
            "summary": summary,
            "keyEvents": key_events if key_events else []
        }
    
    def close_connection(self):
        """Closes the database connection."""
        self.cursor.close()
        self.conn.close()
        print("Database connection closed.")
    
    @kernel_function
    async def get_related_games_diskann(self, embedding_text: str, limit: int = 50) -> List[Tuple[int, List[float]]]:
        """Returns the most similar games to the question using diskann index."""
 
        embedding_service = AzureTextEmbedding(
            deployment_name=" text-embedding-ada-002",
            api_key= os.getenv('AZURE_OPENAI_KEY'),
            endpoint= os.getenv('AZURE_OPENAI_EMBED_ENDPOINT'),
            base_url= os.getenv('AZURE_OPENAI_BASE_EMBED_URL'))
        
        embedding_vector = (await embedding_service.generate_embeddings([embedding_text]))[0]

        embedding = str(embedding_vector.tolist())

        register_vector(self.conn)
        self.cursor.execute(
            """
            SELECT * FROM games_embeddings_diskann
            ORDER BY embedding_vector <-> %s
            LIMIT %s;
            """,
            (embedding, limit)
        )
        
        rows = self.cursor.fetchall()
        return rows
