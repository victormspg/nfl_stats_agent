import urllib.parse
import os
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Load environment variables from .env file, overriding existing ones if necessary
load_dotenv(override=True)

def get_football_connection_uri():
    """
    Builds a PostgreSQL connection URI for the football database using Azure AD authentication.
    """
    dbhost = os.getenv('POSTGRES_HOST')
    dbname = os.getenv('POSTGRES_FOOTBALL_DB')
    dbuser = urllib.parse.quote(os.getenv('POSTGRES_USER'))
    sslmode = os.getenv('SSLMODE')
    dbport = os.getenv('POSTGRES_PORT')

    # Acquire an Azure AD access token for PostgreSQL using DefaultAzureCredential.
    # Note: For production, persist and reuse the credential to benefit from token caching.
    credential = DefaultAzureCredential()
    token = credential.get_token("https://ossrdbms-aad.database.windows.net/.default").token
    password_encoded = urllib.parse.quote_plus(token)

    db_uri = f"postgresql://{dbuser}:{password_encoded}@{dbhost}:{dbport}/{dbname}?sslmode={sslmode}"
    print("Football connection URI retrieved successfully.")
    return db_uri

def get_history_chat_connection_uri():
    """
    Builds a PostgreSQL connection URI for the chat history database using Azure AD authentication.
    """
    dbhost = os.getenv('POSTGRES_HOST')
    dbname = os.getenv('POSTGRES_CHAT_HISTORY_DB')
    dbuser = urllib.parse.quote(os.getenv('POSTGRES_USER'))
    sslmode = os.getenv('SSLMODE')
    dbport = os.getenv('POSTGRES_PORT')

    # Acquire an Azure AD access token for PostgreSQL using DefaultAzureCredential.
    # Note: For production, persist and reuse the credential to benefit from token caching.
    credential = DefaultAzureCredential()
    token = credential.get_token("https://ossrdbms-aad.database.windows.net/.default").token
    password_encoded = urllib.parse.quote_plus(token)

    db_uri = f"postgresql://{dbuser}:{password_encoded}@{dbhost}:{dbport}/{dbname}?sslmode={sslmode}"
    print("Chat history connection URI retrieved successfully.")
    return db_uri
