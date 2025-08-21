import asyncio
import random
import psycopg2
from functools import partial

from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.agents import Agent, ChatCompletionAgent, OrchestrationHandoffs, HandoffOrchestration
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.contents import AuthorRole, ChatMessageContent

from helpers.db_utils import get_football_connection_uri, get_history_chat_connection_uri
from helpers.chat_utils import ChatHistoryInPostgresDB

# System messages
from agents.master_agent.system_message import MASTER_SYSTEM_MESSAGE
from agents.game_analyst.system_message import GAME_ANALYST_SYSTEM_MESSAGE
from agents.player_analyst.system_message import PLAYER_ANALYST_SYSTEM_MESSAGE
from agents.formation_strategist.system_message import FORMATION_STRATEGIST_SYSTEM_MESSAGE

# Plugins
from agents.master_agent.plugins.master_agent_plugin import MasterAgentPlugin
from agents.game_analyst.plugins.game_analyst_plugin import GameAnalystPlugin
from agents.player_analyst.plugins.player_analyst_plugin import PlayerAnalystPlugin
from agents.formation_strategist.plugins.formation_strategist_plugin import FormationStrategistPlugin


# -------------------------------
# Intent Classification
# -------------------------------
INTENT_AGENT_MAP = {
    "game": "GameAnalystAgent",
    "player": "PlayerAnalystAgent",
    "formation": "FormationStrategistAgent",
    "general": "MasterAgent"
}

def classify_intent(user_input: str) -> str:
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


# -------------------------------
# Agent Setup with Handoffs
# -------------------------------
def get_agents_with_handoffs(football_connection_uri) -> tuple[list[Agent], OrchestrationHandoffs]:
    master_plugin = MasterAgentPlugin()
    game_plugin = GameAnalystPlugin(football_connection_uri)
    player_plugin = PlayerAnalystPlugin(football_connection_uri)
    formation_plugin = FormationStrategistPlugin(football_connection_uri)

    master_agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="MasterAgent",
        description="Agent to have conversation with the user and delegate tasks to other specialized agents.",
        plugins=[master_plugin],
        instructions=MASTER_SYSTEM_MESSAGE,
    )

    game_agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="GameAnalystAgent",
        description="Responsible for analyzing game data and providing insights.",
        plugins=[game_plugin],
        instructions=GAME_ANALYST_SYSTEM_MESSAGE,
    )

    player_agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="PlayerAnalystAgent",
        description="Responsible for analyzing player data and providing insights.",
        plugins=[player_plugin],
        instructions=PLAYER_ANALYST_SYSTEM_MESSAGE,
    )

    formation_agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="FormationStrategistAgent",
        description="Responsible for analyzing game plays, offensive and defensive formations and recommending strategic adjustments.",
        plugins=[formation_plugin],
        instructions=FORMATION_STRATEGIST_SYSTEM_MESSAGE,
    )

    handoffs = (
        OrchestrationHandoffs()
        .add_many(
            source_agent=master_agent.name,
            target_agents={
                game_agent.name: "Transfer to this agent if the ask is to collect or analyze game data.",
                player_agent.name: "Transfer to this agent if the ask is to collect or analyze player data.",
                formation_agent.name: "Transfer to this agent if the ask is about plays, plays statistics, formations or tactical strategy.",
            },
        )
        .add_many(
            source_agent=game_agent.name,
            target_agents={
                master_agent.name: "Transfer to this agent if the ask is outside game data.",
                player_agent.name: "Transfer to this agent if the ask is about player data.",
                formation_agent.name: "Transfer to this agent if the ask is about plays, plays statistics, formations or tactical strategy.",
            }
        )
        .add_many(
            source_agent=player_agent.name,
            target_agents={
                master_agent.name: "Transfer to this agent if the ask is outside player data.",
                game_agent.name: "Transfer to this agent if the ask is about game data.",
                formation_agent.name: "Transfer to this agent if the ask is about plays, plays statistics, formations or tactical strategy.",
            }
        )
        .add_many(
            source_agent=formation_agent.name,
            target_agents={
                master_agent.name: "Transfer to this agent if the ask is outside formation strategy.",
                game_agent.name: "Transfer to this agent if the ask is about game data.",
                player_agent.name: "Transfer to this agent if the ask is about player data.",
            }
        )
    )

    return [master_agent, game_agent, player_agent, formation_agent], handoffs


# -------------------------------
# Chat History Functions
# -------------------------------
async def human_response_function_with_history(hist) -> ChatMessageContent:
    user_input = input("User (type exit to end the chat): ")
    msg = ChatMessageContent(role=AuthorRole.USER, content=user_input)
    await hist.on_new_message(msg)
    await hist.store_history()
    return msg

async def agent_response_callback_with_history(hist, message: ChatMessageContent):
    if message.content and message.content.strip():
        print(f"{message.name}: \n{message.content}")
        await hist.on_new_message(message)
        await hist.store_history()


# -------------------------------
# Chat Lifecycle
# -------------------------------
def start_chat():
    print("\nWelcome to NFL Analytics Chat!")
    print("You can ask questions about games, players, formations, and strategy based on data from season 2018.")
    print("Type 'exit' to end the chat.\n")
    customer_id = input("Please enter your customer ID: ")
    session_id = input("Please enter your session ID (or press Enter if this is a new chat/topic): ")
    return customer_id, session_id

async def end_chat(hist):
    await hist.store_history()
    print("NOTE: If you would like to continue this chat in the future, use this session ID:", hist.session_id)
    
# -------------------------------
# Main
# -------------------------------
async def main():
    football_connection_uri = get_football_connection_uri()
    history_chat_connection_uri = get_history_chat_connection_uri()

    agents, handoffs = get_agents_with_handoffs(football_connection_uri)

    customer_id, session_id = start_chat()

    chat_history_conn = psycopg2.connect(history_chat_connection_uri)
    chat_cur = chat_history_conn.cursor()

    hist = ChatHistoryInPostgresDB(
        session_id=session_id,
        customer_id=customer_id,
        conn=chat_history_conn,
        cur=chat_cur
    )

    history_input = await hist.get_history()
    
    if not history_input:
        print("No previous chat history found for this customer. Starting a new chat session...")
        session_id = f"session_" + str(random.randint(1000, 9999))
        hist = ChatHistoryInPostgresDB(
            session_id=session_id,
            customer_id=customer_id,
            conn=chat_history_conn,
            cur=chat_cur
        )
    print(f"\nCustomer ID: {hist.customer_id}, Session ID: {hist.session_id}\n")

    # Use partial to inject hist into callbacks
    handoff_orchestration = HandoffOrchestration(
        members=agents,
        handoffs=handoffs,
        agent_response_callback=partial(agent_response_callback_with_history, hist),
        human_response_function=partial(human_response_function_with_history, hist),
    )

    runtime = InProcessRuntime()
    runtime.start()

    raw_input = input("How can I help you today? (Type 'exit' to end the chat) > ")
    if raw_input.strip().lower() == "exit":
        await end_chat(hist)
    else:
        # Intent-based routing
        intent = classify_intent(raw_input)
        target_agent_name = INTENT_AGENT_MAP[intent]
        print(f"[Routing] Intent classified as '{intent}' → Routed to {target_agent_name}")

        task_input = {
            "history": history_input,
            "user_input": raw_input,
            "target_agent": target_agent_name
        }

        orchestration_result = await handoff_orchestration.invoke(
            task=str(task_input),
            runtime=runtime,
        )
        value = await orchestration_result.get()
        print(f"** Result: **\n{value}")
        await hist.on_new_message(value)
        await end_chat(hist)

        await runtime.stop_when_idle()
       

if __name__ == "__main__":
    asyncio.run(main())
