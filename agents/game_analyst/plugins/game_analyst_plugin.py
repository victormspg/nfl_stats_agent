import psycopg2
from pandas import DataFrame
from semantic_kernel.functions import kernel_function
from typing import Dict, List, Optional, Tuple
import os
from pgvector.psycopg2 import register_vector
import sys
import os
sys.path.append(os.path.abspath('..'))

from helpers.embeddings_utils import embedding_service

class GameAnalystPlugin:
    def __init__(self, db_uri: str):
        self.db_uri = db_uri
        print("Game Analyst Plugin initialized.")

    def get_game_details(self, gameId: Optional[str] = None):
        query = """SELECT 
                    *
                FROM games
                WHERE (LOWER(gameId) = LOWER(%(gameId)s))
                """
        
        if not gameId:
            print("No game ID provided.")
            return None
        
        try:
            conn = psycopg2.connect(self.db_uri)
            cursor = conn.cursor()

            cursor.execute(query, {"gameId": gameId})
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            if not rows:
                print("No game found for the provided ID.")
                return None
            
            games = DataFrame(rows, columns=columns)
            game = games.to_dict(orient="records")[0]  # Get the first game record

            cursor.close()
            conn.close()

            return {
                "date": game["gamedate"],
                "teams": f"{game['visitorteamabbr']} @ {game['hometeamabbr']}",
                "week": game["week"],
                "startTime": game["gametimeeastern"]
            }

        except Exception as e:
            print(f"Error fetching game information: {e}")
            return None
    
    def get_highlight_key_events(self, gameId: Optional[str] = None):

        query = """SELECT 
                    *
                FROM plays
                WHERE (LOWER(gameId) = LOWER(%(gameId)s))
                """
        if not gameId:
            print("No game ID provided.")
            return []
    
        try:
            conn = psycopg2.connect(self.db_uri)
            cursor = conn.cursor()
            cursor.execute(query, {"gameId": gameId})
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            if not rows:
                print("No plays found for the provided game ID.")
                return []

            plays = [dict(zip(columns, row)) for row in rows]

            key_events = [
                p for p in plays
                if ("touchdown" in p.get("playdescription", "").lower()) or
                (p.get("passresult") in ["IN", "S"])
            ]
            cursor.close()
            conn.close()
            return key_events

        except Exception as e:
            print(f"Error fetching play data: {e}")
            return []

    @kernel_function 
    def get_game_summary(self, gameId: Optional[str] = None) -> dict:
        summary = self.get_game_details(gameId)
        key_events = self.get_highlight_key_events(gameId)
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

    @kernel_function
    def get_teams_results(self, teams: List[str]) -> List[Dict]:
        """
        Returns the game results for specific teams.
        """
        teams_str = ','.join(f"'{item}'" for item in teams)

        query = f"""
        SELECT week, gamedate, gametimeeastern, t.hometeamabbr, t.visitorteamabbr, t.presnaphomescore, t.presnapvisitorscore 
        FROM (
            SELECT 
                week, 
                gamedate,
                gametimeeastern,
                hometeamabbr, 
                visitorteamabbr, 
                presnaphomescore, 
                presnapvisitorscore,
                ROW_NUMBER() OVER (
                    PARTITION BY week, hometeamabbr, visitorteamabbr 
                    ORDER BY presnaphomescore DESC, presnapvisitorscore DESC
                ) AS rn
            FROM games
            JOIN plays USING (gameid)
            WHERE (
                UPPER(hometeamabbr) IN ({teams_str}) OR 
                UPPER(visitorteamabbr) IN ({teams_str})
            )
            AND (
                presnaphomescore IS NOT NULL OR 
                presnapvisitorscore IS NOT NULL
            )
        ) t
        WHERE rn = 1;
        """
        
        try:
            conn = psycopg2.connect(self.db_uri)
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f"Error fetching teams game results: {e}")
            return []
    
    @kernel_function
    async def get_related_games_diskann(self, embedding_text: str, limit: int = 100) -> List[Tuple[int, List[float]]]:
        """Returns the most similar games to the question using diskann index."""
        
        embedding_vector = (await embedding_service.generate_embeddings([embedding_text]))[0]

        embedding = str(embedding_vector.tolist())

        conn = psycopg2.connect(self.db_uri)
        cursor = conn.cursor()

        register_vector(cursor)
        cursor.execute(
            """
            SELECT * FROM games_embeddings_diskann
            ORDER BY embedding_vector <-> %s
            LIMIT %s;
            """,
            (embedding, limit)
        )
        
        rows = cursor.fetchall()
        return rows
