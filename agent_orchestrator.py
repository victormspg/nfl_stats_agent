from semantic_kernel.kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.agents import ChatCompletionAgent
from helpers.db_utils import get_football_connection_uri, get_history_chat_connection_uri
from helpers.chat_utils import start_chat
from agents.game_analyst.system_message import GAME_ANALYSIS_SYSTEM_MESSAGE
from agents.game_analyst.plugins.game_analyst_plugin import GameAnalystPlugin
import random,psycopg2, asyncio



if __name__ == "__main__":
    sk = Kernel()
    football_connection_uri = get_football_connection_uri()
    history_chat_connection_uri = get_history_chat_connection_uri()
    
    game_analyst_agent_plugin = GameAnalystPlugin(football_connection_uri)

    game_analyst_agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="GameAnalystAgent",
        kernel=sk,
        instructions=GAME_ANALYSIS_SYSTEM_MESSAGE,
        plugins=[game_analyst_agent_plugin],
    )

    import asyncio
    asyncio.run(start_chat(game_analyst_agent, history_chat_connection_uri))
