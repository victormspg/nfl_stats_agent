from semantic_kernel.connectors.ai.open_ai import AzureTextEmbedding
import os
from dotenv import load_dotenv
load_dotenv(override=True)

embedding_service = AzureTextEmbedding(
    deployment_name=" text-embedding-ada-002",
    api_key= os.getenv('AZURE_OPENAI_KEY'),
    endpoint= os.getenv('AZURE_OPENAI_EMBED_ENDPOINT'),
    base_url= os.getenv('AZURE_OPENAI_BASE_EMBED_URL')
)
