import os
import libsql_client


url = os.environ.get("TURSO_DATABASE_URL")
auth_token = os.environ.get("TURSO_AUTH_TOKEN")

client = create_client(
    url=url,
    auth_token=auth_token
)

def ejecutar(query: str, params=None):
    if params is None:
        params = []

    return client.execute(query, params)