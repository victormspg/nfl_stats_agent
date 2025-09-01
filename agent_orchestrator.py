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

# System messages for each agent
from agents.master_agent.system_message import MASTER_SYSTEM_MESSAGE
from agents.game_analyst.system_message import GAME_ANALYST_SYSTEM_MESSAGE
from agents.player_analyst.system_message import PLAYER_ANALYST_SYSTEM_MESSAGE
from agents.formation_strategist.system_message import FORMATION_STRATEGIST_SYSTEM_MESSAGE

# Plugins for each agent
from agents.master_agent.plugins.master_agent_plugin import MasterAgentPlugin
from agents.game_analyst.plugins.game_analyst_plugin import GameAnalystPlugin
from agents.player_analyst.plugins.player_analyst_plugin import PlayerAnalystPlugin
from agents.formation_strategist.plugins.formation_strategist_plugin import FormationStrategistPlugin

# -------------------------------
# Intent Classification
# -------------------------------

# Maps intent keywords to agent names
INTENT_AGENT_MAP = {
    "game": "GameAnalystAgent",
    "player": "PlayerAnalystAgent",
    "formation": "FormationStrategistAgent",
    "general": "MasterAgent"
}

def classify_intent(user_input: str) -> str:
    """
    Classifies the user's input into one of the supported intents
    based on keyword matching.
    """
    user_input_lower = user_input.lower()

    # Keywords for each intent
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

    # Check for keywords in user input
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
    """
    Instantiates all agents and sets up handoff rules between them.
    Returns a list of agents and the orchestration handoffs object.
    """
    # Instantiate plugins for each agent
    master_plugin = MasterAgentPlugin()
    game_plugin = GameAnalystPlugin(football_connection_uri)
    player_plugin = PlayerAnalystPlugin(football_connection_uri)
    formation_plugin = FormationStrategistPlugin(football_connection_uri)

    # Create each agent with its plugin and system message
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

    # Define handoff rules between agents
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
    """
    Prompts the user for input, stores the message in chat history,
    and returns a ChatMessageContent object.
    """
    user_input = input("User (type exit to end the chat): ")
    msg = ChatMessageContent(role=AuthorRole.USER, content=user_input)
    await hist.on_new_message(msg)
    await hist.store_history()
    return msg

async def agent_response_callback_with_history(hist, message: ChatMessageContent):
    """
    Handles agent responses: prints them, stores them in chat history.
    """
    if message.content and message.content.strip():
        print(f"{message.name}: \n{message.content}")
        await hist.on_new_message(message)
        await hist.store_history()

# -------------------------------
# Chat Lifecycle
# -------------------------------

def start_chat():
    """
    Greets the user and collects customer/session IDs.
    """
    print("\n🏈 Welcome to NFL Analytics Assistant!")
    print("Ask about games, players, formations, or strategy from the 2018 NFL season.")
    print("Type 'exit' to end the chat.\n")
    customer_id = input("Please enter your User ID: ")
    session_id = input("Please enter your Session ID (or press Enter if this is a new chat/topic): ")
    return customer_id, session_id

async def end_chat(hist):
    """
    Stores chat history and informs the user about the session ID.
    """
    await hist.store_history()
    print("NOTE: If you would like to continue this chat in the future, use this session ID:", hist.session_id)
    
# -------------------------------
# Main
# -------------------------------

async def main():
    """
    Main entry point for the chat assistant.
    Sets up agents, chat history, and orchestrates the conversation.
    """
    football_connection_uri = get_football_connection_uri()
    history_chat_connection_uri = get_history_chat_connection_uri()

    # Set up agents and handoff rules
    agents, handoffs = get_agents_with_handoffs(football_connection_uri)

    # Start chat and get user/customer/session info
    customer_id, session_id = start_chat()

    # Connect to chat history database
    chat_history_conn = psycopg2.connect(history_chat_connection_uri)
    chat_cur = chat_history_conn.cursor()

    # Initialize chat history object
    hist = ChatHistoryInPostgresDB(
        session_id=session_id,
        customer_id=customer_id,
        conn=chat_history_conn,
        cur=chat_cur
    )

    # Retrieve previous chat history if available
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
    print(f"\nUser ID: {hist.customer_id}, Session ID: {hist.session_id}\n")

    # Set up orchestration with callbacks for agent/human responses
    handoff_orchestration = HandoffOrchestration(
        members=agents,
        handoffs=handoffs,
        agent_response_callback=partial(agent_response_callback_with_history, hist),
        human_response_function=partial(human_response_function_with_history, hist),
    )

    # Start the agent runtime
    runtime = InProcessRuntime()
    runtime.start()

    # Prompt user for initial input
    raw_input = input("How can I help you today? (Type 'exit' to end the chat) > ")
    if raw_input.strip().lower() == "exit":
        await end_chat(hist)
    else:
        # Classify intent and route to the appropriate agent
        intent = classify_intent(raw_input)
        target_agent_name = INTENT_AGENT_MAP[intent]
        print(f"[Routing] Intent classified as '{intent}' → Routed to {target_agent_name}")

        # Prepare task input for orchestration
        task_input = {
            "history": history_input,
            "user_input": raw_input,
            "target_agent": target_agent_name
        }

        # Invoke orchestration and handle result
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
