# Import the AzureTextEmbedding class from Semantic Kernel's OpenAI connector
from semantic_kernel.connectors.ai.open_ai import AzureTextEmbedding
import os
from dotenv import load_dotenv

# Load environment variables from a .env file, overriding existing ones if necessary
load_dotenv(override=True)

# Initialize the AzureTextEmbedding service with configuration from environment variables
embedding_service = AzureTextEmbedding(
    deployment_name="text-embedding-ada-002",  # Name of the Azure OpenAI embedding deployment
    api_key=os.getenv('AZURE_OPENAI_KEY'),     # API key for Azure OpenAI
    endpoint=os.getenv('AZURE_OPENAI_EMBED_ENDPOINT'),  # Endpoint URL for the embedding service
    base_url=os.getenv('AZURE_OPENAI_BASE_EMBED_URL')   # Optional base URL for the embedding service
)
