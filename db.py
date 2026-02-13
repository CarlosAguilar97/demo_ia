import os
from libsql_client import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("TURSO_DATABASE_URL")
auth_token = os.getenv("TURSO_AUTH_TOKEN")

client = create_client(
    url=url,
    auth_token=auth_token
)

def ejecutar(query: str, params=None):
    if params is None:
        params = []

    return client.execute(query, params)