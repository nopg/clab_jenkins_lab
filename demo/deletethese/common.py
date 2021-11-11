"""common"""
import os
from typing import Optional

import httpx
import hvac
from scrapli import AsyncScrapli

# Set to False if running locally, True if running in the container
DOCKER = True
SERVICE_ACCOUNT_PASSWORD = os.environ.get("SERVICE_PASS", "service")

VAULT_HOST = "http://172.20.0.99:8888" if DOCKER else "http://localhost:8888"
VAULT_CLIENT: Optional[hvac.Client] = None

NETBOX_HOST_LOCALHOST = "http://localhost:8000"
NETBOX_HOST = "http://172.20.0.101:8080" if DOCKER else NETBOX_HOST_LOCALHOST
NETBOX_TOKEN = "0123456789abcdef0123456789abcdef01234567"

DEVICE_IP_PORT_MAP = {
    "spine1": (
        "172.20.0.11",
        22 if DOCKER else 2211,
    ),
    "spine2": (
        "172.20.0.12",
        22 if DOCKER else 2212,
    ),
    "leaf1": (
        "172.20.0.21",
        22 if DOCKER else 2221,
    ),
    "leaf2": (
        "172.20.0.22",
        22 if DOCKER else 2222,
    ),
}


async def get_vault_client() -> hvac.Client:
    """
    Return a vault client, create it if it is not currently set

    Args:
        N/A

    Returns:
        hvac.Client: vault client

    Raises:
        Exception: if we can't create the client

    """
    # not pretty, but cheap/fast singleton for the client
    global VAULT_CLIENT

    if VAULT_CLIENT is None:
        vault_client_token = await get_vault_client_token()
        client = hvac.Client(f"{VAULT_HOST}", token=vault_client_token)
        if not client.is_authenticated():
            raise Exception("ruhroh, couldn't get auth'd to vault :(")
        VAULT_CLIENT = client

    return VAULT_CLIENT


async def get_vault_client_token() -> str:
    """
    Fetch a vault client token for the service account

    Args:
        N/A

    Returns:
        str: token to use for vault client auth

    Raises:
        Exception: if we fail to fetch the token

    """
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{VAULT_HOST}/v1/auth/userpass/login/service",
            data={"password": SERVICE_ACCOUNT_PASSWORD},
        )

    if resp.status_code != 200:
        raise Exception("failed to fetch token for vault auth")

    return resp.json().get("auth", {}).get("client_token", "")


async def get_service_account_password() -> str:
    """
    Get the password for the service account from vault

    Args:
        N/A

    Returns:
        str: service account password

    Raises:
        N/A

    """
    client = await get_vault_client()
    secret_data = client.secrets.kv.v2.read_secret_version(
        mount_point="service_credentials", path="clos_access"
    )

    return secret_data.get("data", {}).get("data", {}).get("password", "")


async def get_user_account_password() -> str:
    """
    Get the password for the user account from vault

    Args:
        N/A

    Returns:
        str: user account password

    Raises:
        N/A

    """
    client = await get_vault_client()
    secret_data = client.secrets.kv.v2.read_secret_version(
        mount_point="network_credentials", path="clos_access"
    )

    return secret_data.get("data", {}).get("data", {}).get("password", "")


async def open_connection(connection: AsyncScrapli) -> bool:
    """
    Open a scrapli connection to a device

    Args:
        connection: scrapli connection object to open

    Returns:
        bool: True if connection is opened successfully, otherwise False

    Raises:
        N/A

    """
    try:
        await connection.open()
    except Exception as exc:
        print(f"encountered exception opening connection to {connection.host}; execption: {exc}")
        return False
    return True
