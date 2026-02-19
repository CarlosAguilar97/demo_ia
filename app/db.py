import os
from libsql_client import create_client


def get_client():
    url = os.environ.get("TURSO_DATABASE_URL")
    auth_token = os.environ.get("TURSO_AUTH_TOKEN")

    return create_client(
        url=url,
        auth_token=auth_token
    )


def ejecutar(query: str, params=None):
    if params is None:
        params = []

    client = get_client()  # ✅ crear conexión por request (serverless-safe)
    return client.execute(query, params)