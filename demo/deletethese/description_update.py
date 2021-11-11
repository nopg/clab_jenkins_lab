"""description_update"""
import asyncio
import sys
import warnings

import httpx
from scrapli import AsyncScrapli
from scrapli_cfg import AsyncScrapliCfg

from common import (
    DEVICE_IP_PORT_MAP,
    NETBOX_HOST,
    NETBOX_TOKEN,
    get_service_account_password,
    open_connection,
)

# filtering warnings to ignore scrapli auth_secondary warning since we have no auth secondary set!
warnings.filterwarnings("ignore")


async def get_device_from_id(device_id: str) -> str:
    """
    Get device hostname from provided device id

    Args:
        device_id: id of device to fetch

    Returns:
        str: hostname of the device with the given id

    Raises:
        ValueError: if id not in netbox

    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{NETBOX_HOST}/api/dcim/devices/{device_id}/",
            headers={"Authorization": f"Token {NETBOX_TOKEN}"},
        )

    if resp.status_code != 200:
        raise Exception("failed to fetch device info")

    return resp.json().get("name", "")


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
    device_id, intf_id, intf_name, intf_desc = sys.argv[1:]

    if not all((device_id, intf_id, intf_name, intf_desc)):
        print("cannot continue, didn't get all the required parameters from netbox/jenkins")
        sys.exit(1)

    service_account_password = await get_service_account_password()

    hostname = await get_device_from_id(device_id=device_id)  # type: ignore
    ip_port = DEVICE_IP_PORT_MAP.get(hostname)

    if not ip_port:
        print(f"cannot continue, hostname not found  {hostname}")
        sys.exit(1)

    connection = AsyncScrapli(
        host=ip_port[0],
        port=ip_port[1],
        auth_username="admin",
        auth_password=service_account_password,
        auth_strict_key=False,
        transport="asyncssh",
        platform="arista_eos",
    )

    open_result = await open_connection(connection)

    if open_result is False:
        print("cannot continue, could not login to all devices :(")
        sys.exit(1)

    async with AsyncScrapliCfg(conn=connection) as cfg_conn:
        await cfg_conn.load_config(
            config=f"interface {intf_name}\ndescription {intf_desc}", replace=False
        )
        diff = await cfg_conn.diff_config()
        await cfg_conn.commit_config()

    print("job complete, printing diff:")
    print(diff.device_diff)


if __name__ == "__main__":
    asyncio.run(main())
