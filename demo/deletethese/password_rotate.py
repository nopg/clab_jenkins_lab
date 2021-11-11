"""password_rotate"""
import asyncio
import sys
import warnings
from random import randint

from scrapli import AsyncScrapli

from common import (
    DEVICE_IP_PORT_MAP,
    get_service_account_password,
    get_vault_client,
    open_connection,
)

# filtering warnings to ignore scrapli auth_secondary warning since we have no auth secondary set!
warnings.filterwarnings("ignore")

PASSWORD_WORDS = (
    "taco",
    "cat",
    "potato",
    "onion",
    "car",
    "hat",
)


def generate_password() -> str:
    """
    Generate a stupid password from our list of password words

    Args:
        N/A

    Returns:
        str: our new silly password

    Raises:
        N/A

    """
    return (
        PASSWORD_WORDS[randint(0, len(PASSWORD_WORDS) - 1)]
        + "-"
        + PASSWORD_WORDS[randint(0, len(PASSWORD_WORDS) - 1)]
    )


async def update_user_account_password(password: str) -> None:
    """
    Create a new secret version for the user account, setting the new password value

    Args:
        password: password to update in vault

    Returns:
        N/A

    Raises:
        N/A

    """
    client = await get_vault_client()
    update_data = client.secrets.kv.v2.create_or_update_secret(
        mount_point="network_credentials",
        path="clos_access",
        secret={"username": "carl", "password": password},
    )

    new_secret_verion = update_data.get("data", {}).get("version", -1)
    if new_secret_verion != -1:
        print(f"user network credentials update, new secret version is {new_secret_verion}")


async def update_network_device_password(connection: AsyncScrapli, password: str) -> bool:
    """
    Update the user password on a network device

    Args:
        connection: scrapli connection
        passwrod: new password value

    Returns:
        bool: True if things work out nicely... otherwise False

    Raises:
        N/A

    """
    result = await connection.send_config(f"username carl privilege 15 secret {password}")
    if result.failed is True:
        return False
    return True


async def main() -> None:
    """
    Silly demo app that rotates passwords for a user

    Apologies for some bad code, please chill, its just a demo :D

    Args:
        N/A

    Returns:
        N/A

    Raises:
        N/A

    """
    service_account_password = await get_service_account_password()

    connections = {
        hostname: AsyncScrapli(
            host=ip_port[0],
            port=ip_port[1],
            auth_username="admin",
            auth_password=service_account_password,
            auth_strict_key=False,
            transport="asyncssh",
            platform="arista_eos",
        )
        for hostname, ip_port in DEVICE_IP_PORT_MAP.items()
    }
    open_results = await asyncio.gather(
        *[open_connection(connection) for connection in connections.values()]
    )

    if any(result is False for result in open_results):
        print("cannot continue, could not login to all devices :(")
        sys.exit(1)

    new_password = generate_password()

    update_results = await asyncio.gather(
        *[
            update_network_device_password(connection=connection, password=new_password)
            for connection in connections.values()
        ]
    )

    for host, update_result in zip(connections.keys(), update_results):
        if update_result is False:
            print(f"failed updating password on host {host}")
        else:
            print(f"update password on host {host} -> {new_password}")

    await update_user_account_password(password=new_password)


if __name__ == "__main__":
    asyncio.run(main())
