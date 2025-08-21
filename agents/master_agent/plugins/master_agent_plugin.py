import json
import re
from typing import Dict
from semantic_kernel.functions import kernel_function

class MasterAgentPlugin:
    def __init__(self):
        print("Master Agent Plugin initialized.")

    # 1️⃣ Classify user intent
    @kernel_function
    def classify_user_intent(self, user_input: str) -> str:
        """
        Classifies user intent based on keywords.
        Returns one of: 'game', 'player', 'formation', 'general'
        """
        user_input_lower = user_input.lower()
        
        formation_keywords = [
            "play", "formation", "playbook", "offense", "defense", "strategy", "tactical",
            "epa", "dropback", "blitz", "coverage", "zone", "man-to-man", "scheme",
            "alignment", "motion", "read", "gap", "contain", "rush", "package", "adjustment"
        ]

        player_keywords = [
            "player", "stats", "statistics", "speed", "acceleration", "route", "nflid",
            "profile", "combine", "draft", "height", "weight", "position", "injury",
            "performance", "rating", "grade", "scouting", "talent", "metrics", "bio"
        ]

        game_keywords = [
            "game", "matchup", "score", "week", "team", "schedule", "kickoff", "result",
            "final", "quarter", "halftime", "drive", "possession", "win", "loss",
            "record", "standings", "opponent", "fixture", "broadcast", "venue"
        ]

        if any(keyword in user_input_lower for keyword in formation_keywords):
            return "formation"
        elif any(keyword in user_input_lower for keyword in player_keywords):
            return "player"
        elif any(keyword in user_input_lower for keyword in game_keywords):
            return "game"
        else:
            return "general"

    # 2️⃣ Summarize agent response
    @kernel_function
    def summarize_agent_response(self, agent_name: str, response: Dict) -> str:
        """
        Converts structured agent output into a user-friendly summary.
        """
        summary = f"Response from {agent_name}:\n"
        if isinstance(response, dict):
            for key, value in response.items():
                if isinstance(value, list):
                    summary += f"- {key}: {', '.join(str(v) for v in value)}\n"
                else:
                    summary += f"- {key}: {value}\n"
        else:
            summary += str(response)
        return summary.strip()

    # 3️⃣ Track agent usage
    @kernel_function
    def track_agent_usage(self, session_id: str, agent_name: str, query: str) -> str:
        """
        Logs which agent handled which query. (Simulated logging)
        """
        log_entry = {
            "session_id": session_id,
            "agent": agent_name,
            "query": query
        }
        print(f"[LOG] Agent usage tracked: {json.dumps(log_entry)}")
        return "Agent usage logged."

    # 4️⃣ Resolve ambiguous query
    @kernel_function
    def resolve_ambiguous_query(self, user_input: str) -> str:
        """
        Reformulates vague queries and asks for clarification.
        """
        if len(user_input.strip().split()) < 4:
            return f"Your question seems a bit vague: '{user_input}'. Could you clarify what you're asking about—game, player, or formation?"
        if not re.search(r"\b(game|player|formation)\b", user_input.lower()):
            return f"I'm not sure which domain your question relates to. Could you specify if it's about a game, a player, or a formation?"
        return "Query appears sufficiently clear."