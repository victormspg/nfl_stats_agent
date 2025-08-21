import psycopg2
from pandas import DataFrame
from semantic_kernel.functions import kernel_function
from typing import List, Optional, Tuple, Dict 
import os
from pgvector.psycopg2 import register_vector
import sys
import os

sys.path.append(os.path.abspath('..'))

from helpers.embeddings_utils import embedding_service

class FormationStrategistPlugin:
    def __init__(self, db_uri: str):
        self.db_uri = db_uri
        print("Formation Strategist Plugin initialized.")

    @kernel_function
    def get_plays_from_a_game(self, gameId: Optional[str] = None) -> dict:
        query = """SELECT 
                        *
                    FROM plays
                    WHERE (LOWER(gameid) = LOWER(%(gameId)s))
                    """
        if not gameId:
            print("No Game ID provided.")
            return None
    
        try:
            conn = psycopg2.connect(self.db_uri)
            cursor = conn.cursor()
            cursor.execute(query, {"gameId": gameId})
            plays = cursor.fetchall()

            if not plays:
                print(f"No plays found for Game ID '{gameId}'.")
                return None

            return plays

        except Exception as e:
            print(f"Error fetching player profile: {e}")
            return None

    @kernel_function
    async def get_related_plays_diskann(self, embedding_text: str, limit: int = 100) -> List[Tuple[int, List[float]]]:
        """Returns the most similar plays to the question using diskann index."""

        embedding_vector = (await embedding_service.generate_embeddings([embedding_text]))[0]

        embedding = str(embedding_vector.tolist())

        conn = psycopg2.connect(self.db_uri)
        cursor = conn.cursor()
        
        register_vector(conn)
        cursor.execute(
            """
            SELECT * FROM plays_embeddings_diskann
            ORDER BY embedding_vector <-> %s
            LIMIT %s;
            """,
            (embedding, limit)
        )
        
        rows = cursor.fetchall()
        return rows
