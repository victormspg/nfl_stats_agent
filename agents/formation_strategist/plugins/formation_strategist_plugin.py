import psycopg2
from pandas import DataFrame
from semantic_kernel.functions import kernel_function
from typing import List, Optional, Tuple, Dict 
import os
from pgvector.psycopg2 import register_vector
import sys

# Add parent directory to sys.path to import helpers
sys.path.append(os.path.abspath('..'))

from helpers.embeddings_utils import embedding_service

class FormationStrategistPlugin:
    def __init__(self, db_uri: str):
        """
        Initialize the plugin with the database URI.
        """
        self.db_uri = db_uri
        print("Formation Strategist Plugin initialized.")

    @kernel_function
    def get_plays_from_a_game(self, gameId: Optional[str] = None) -> dict:
        """
        Fetch all plays from the database for a given game ID.

        Args:
            gameId (str, optional): The ID of the game to fetch plays for.

        Returns:
            dict: List of plays or None if not found.
        """
        query = """
            SELECT *
            FROM plays
            WHERE (LOWER(gameid) = LOWER(%(gameId)s))
        """
        if not gameId:
            print("No Game ID provided.")
            return None
    
        try:
            # Connect to the PostgreSQL database
            conn = psycopg2.connect(self.db_uri)
            cursor = conn.cursor()
            # Execute the query with the provided gameId
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
        """
        Returns the most similar plays to the question using the diskann index.

        Args:
            embedding_text (str): The text to generate the embedding for similarity search.
            limit (int): Number of similar plays to return.

        Returns:
            List[Tuple[int, List[float]]]: List of similar plays and their embeddings.
        """
        # Generate embedding vector for the input text
        embedding_vector = (await embedding_service.generate_embeddings([embedding_text]))[0]
        embedding = str(embedding_vector.tolist())

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(self.db_uri)
        cursor = conn.cursor()
        
        # Register pgvector extension for vector operations
        register_vector(conn)
        # Query the plays_embeddings_diskann table for similar embeddings
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
