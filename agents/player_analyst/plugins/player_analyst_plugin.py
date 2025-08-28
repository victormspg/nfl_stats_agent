import psycopg2
from pandas import DataFrame
from semantic_kernel.functions import kernel_function
from typing import List, Optional, Tuple, Dict
import os
from pgvector.psycopg2 import register_vector
import sys

sys.path.append(os.path.abspath('..'))

from helpers.embeddings_utils import embedding_service

class PlayerAnalystPlugin:
    def __init__(self, db_uri: str):
        """
        Initialize the PlayerAnalystPlugin with a database URI.
        """
        self.db_uri = db_uri
        print("Player Analyst Plugin initialized.")

    @kernel_function
    def get_player_profile(self, nflId: Optional[str] = None) -> dict:
        """
        Retrieve a player's profile information from the database using their NFL ID.
        """
        query = """SELECT 
                        *
                    FROM players
                    WHERE (LOWER(nflid) = LOWER(%(nflId)s))
                    """
        if not nflId:
            print("No NFL ID provided.")
            return None
    
        try:
            conn = psycopg2.connect(self.db_uri)
            cursor = conn.cursor()
            cursor.execute(query, {"nflId": nflId})
            row = cursor.fetchone()
            columns = [desc[0] for desc in cursor.description]

            if not row:
                print(f"No player found for NFL ID '{nflId}'.")
                return None

            player = dict(zip(columns, row))

            # Return selected profile fields
            return {
                "name": player["displayname"],
                "position": player["position"],
                "height": player["height"],
                "weight": player["weight"],
                "college": player["collegename"]
            }

        except Exception as e:
            print(f"Error fetching player profile: {e}")
            return None

    @kernel_function
    def get_player_stats_per_game(self, nflId: Optional[str] = None, gameId: Optional[str] = None, playId: Optional[str] = None) -> dict:
        """
        Retrieve and aggregate a player's movement stats for a specific game and play.
        """
        if not nflId or not gameId or not playId:
            print("nflId, gameId, and playId are required.")
            return {}

        query = """
            SELECT time, x, y, s, a, dis, o, dir, event, displayname, jerseynumber,
                position, team, frameid, playid, playdirection, route
            FROM week_data
            WHERE CAST(nflid AS FLOAT) = CAST(%(nflId)s AS FLOAT) AND LOWER(gameid) = LOWER(%(gameId)s) AND CAST(playid AS INT) = CAST(%(playId)s AS INT)
        """

        try:
            conn = psycopg2.connect(self.db_uri)
            cursor = conn.cursor()
            cursor.execute(query, {"nflId": nflId, "gameId": gameId, "playId": playId})
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            if not rows:
                print(f"No data found for player {nflId} in game {gameId}.")
                return {}

            data = [dict(zip(columns, row)) for row in rows]

            # Aggregate stats across all frames for the play
            total_distance = sum(d["dis"] for d in data)
            avg_speed = sum(d["s"] for d in data) / len(data)
            max_speed = max(d["s"] for d in data)
            avg_acceleration = sum(d["a"] for d in data) / len(data)
            max_acceleration = max(d["a"] for d in data)

            # Collect unique events, routes, and play IDs
            events = list(set(d["event"] for d in data if d["event"]))
            routes = list(set(d["route"] for d in data if d["route"]))
            play_ids = set(d["playid"] for d in data)
            frame_count = len(data)

            # Use the first row as a sample for static info
            sample = data[0]
            return {
                "playerName": sample["displayname"],
                "jerseyNumber": sample["jerseynumber"],
                "position": sample["position"],
                "team": sample["team"],
                "playDirection": sample["playdirection"],
                "averageSpeed": round(avg_speed, 2),
                "maxSpeed": round(max_speed, 2),
                "averageAcceleration": round(avg_acceleration, 2),
                "maxAcceleration": round(max_acceleration, 2),
                "totalDistance": round(total_distance, 2),
                "frameCount": frame_count,
                "uniquePlays": len(play_ids),
                "events": events,
                "routes": routes
            }

        except Exception as e:
            print(f"Error retrieving stats: {e}")
            return {}

    @kernel_function
    def compare_players_by_stats(self, nflIds: List[str], gameId: str) -> List[Dict]:
        """
        Compare multiple players based on movement metrics in a specific game.
        """
        results = []
        for nflId in nflIds:
            stats = self.get_player_stats_per_game(nflId=nflId, gameId=gameId)
            if stats:
                results.append({
                    "playerName": stats.get("playerName"),
                    "averageSpeed": stats.get("averageSpeed"),
                    "maxSpeed": stats.get("maxSpeed"),
                    "averageAcceleration": stats.get("averageAcceleration"),
                    "maxAcceleration": stats.get("maxAcceleration"),
                    "totalDistance": stats.get("totalDistance"),
                    "uniquePlays": stats.get("uniquePlays")
                })
        return results

        # The following code is unreachable due to the return above.
        # If you want to summarize player events, move this to a separate function.

        """
        Summarize the types and frequency of tagged events for a player in a game.
        """
        query = """
        SELECT event
        FROM week_data
        WHERE CAST(nflid as FLOAT) = CAST(%(nflId)s AS FLOAT) AND LOWER(gameid) = LOWER(%(gameId)s)
        """
        try:
            conn = psycopg2.connect(self.db_uri)
            cursor = conn.cursor()
            cursor.execute(query, {"nflId": nflId, "gameId": gameId})
            rows = cursor.fetchall()
            events = [row[0] for row in rows if row[0]]
            event_counts = {}
            for e in events:
                event_counts[e] = event_counts.get(e, 0) + 1
            return {"nflId": nflId, "gameId": gameId, "eventSummary": event_counts}
        except Exception as e:
            print(f"Error summarizing player events: {e}")
            return {"nflId": nflId, "gameId": gameId, "eventSummary": {}}

    @kernel_function
    def get_player_route_efficiency(self, nflId: str, gameId: str) -> Dict:
        """
        Evaluate route execution efficiency based on speed, acceleration, and distance.
        """
        query = """
        SELECT route, s, a, dis
        FROM week_data
        WHERE CAST(nflid as FLOAT) = CAST(%(nflId)s AS FLOAT) AND LOWER(gameid) = LOWER(%(gameId)s)
        AND route IS NOT NULL
        """
        try:
            conn = psycopg2.connect(self.db_uri)
            cursor = conn.cursor()
            cursor.execute(query, {"nflId": nflId, "gameId": gameId})
            rows = cursor.fetchall()
            route_data = {}
            # Group metrics by route
            for route, speed, accel, dist in rows:
                if route not in route_data:
                    route_data[route] = {"speed": [], "accel": [], "dist": []}
                route_data[route]["speed"].append(speed)
                route_data[route]["accel"].append(accel)
                route_data[route]["dist"].append(dist)

            efficiency = {}
            # Calculate averages and totals for each route
            for route, metrics in route_data.items():
                efficiency[route] = {
                    "avgSpeed": round(sum(metrics["speed"]) / len(metrics["speed"]), 2),
                    "avgAccel": round(sum(metrics["accel"]) / len(metrics["accel"]), 2),
                    "totalDistance": round(sum(metrics["dist"]), 2)
                }

            return {"nflId": nflId, "gameId": gameId, "routeEfficiency": efficiency}
        except Exception as e:
            print(f"Error calculating route efficiency: {e}")
            return {"nflId": nflId, "gameId": gameId, "routeEfficiency": {}}
    
    @kernel_function
    async def get_related_players_diskann(self, embedding_text: str, limit: int = 100) -> List[Tuple[int, List[float]]]:
        """
        Returns the most similar players to the input text using a diskann index on player embeddings.
        """
        # Generate embedding for the input text
        embedding_vector = (await embedding_service.generate_embeddings([embedding_text]))[0]
        embedding = str(embedding_vector.tolist())

        conn = psycopg2.connect(self.db_uri)
        cursor = conn.cursor()
        
        # Register vector extension for similarity search
        register_vector(conn)
        cursor.execute(
            """
            SELECT * FROM players_embeddings_diskann
            ORDER BY embedding_vector <-> %s
            LIMIT %s;
            """,
            (embedding, limit)
        )
        
        rows = cursor.fetchall()
        return rows