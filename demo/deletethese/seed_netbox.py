"""seed_netbox"""
import asyncio
import re
from dataclasses import asdict, dataclass
from typing import Dict, List

import httpx
from typing_extensions import Protocol

from common import NETBOX_HOST_LOCALHOST, NETBOX_TOKEN


class IsDataclass(Protocol):
    __dataclass_fields__: Dict


@dataclass
class NetBoxTag:
    name: str
    slug: str
    color: str
    description: str


@dataclass
class NetBoxManufacturer:
    name: str
    slug: str


@dataclass
class NetBoxDeviceType:
    manufacturer: int
    model: str
    slug: str


@dataclass
class NetBoxDeviceRoles:
    name: str
    slug: str
    color: str
    description: str


@dataclass
class NetBoxRegions:
    name: str
    slug: str


@dataclass
class NetBoxSites:
    name: str
    slug: str
    status: str
    region: int


@dataclass
class NetBoxLocations:
    name: str
    slug: str
    site: int


@dataclass
class NetBoxDevices:
    name: str
    device_type: int
    device_role: int
    manufacturer: int
    site: int
    location: int
    tags: List[Dict[str, str]]


@dataclass
class NetBoxInterfaces:
    device: int
    name: str
    type: str = "other"
    enabled: bool = True
    mgmt_only: bool = False
    mark_connected: bool = True


@dataclass
class NetBoxIpAddresses:
    address: str
    assigned_object_id: int
    description: str
    tags: List[Dict[str, str]]
    status: str = "active"
    assigned_object_type: str = "dcim.interface"
    role: str = ""


@dataclass
class NetBoxCables:
    termination_a_id: int
    termination_b_id: int
    termination_a_type: str = "dcim.interface"
    termination_b_type: str = "dcim.interface"


@dataclass
class NetBoxWebHooks:
    name: str
    payload_url: str
    additional_headers: str
    content_types: List[str]
    type_update: bool = True
    enabled: bool = True
    http_method: str = "POST"
    ssl_verification: bool = False


TAGS = [
    NetBoxTag(name="dc-even", slug="dc-even", color="05195c", description="dc even switches"),
    NetBoxTag(name="dc-odd", slug="dc-odd", color="0531e1", description="dc odd switches"),
    NetBoxTag(
        name="management-interface-ip",
        slug="management-interface-ip",
        color="f93030",
        description="device management interface ip",
    ),
]

MANUFACTURERS = [NetBoxManufacturer(name="arista", slug="arista")]

DEVICE_TYPES = [NetBoxDeviceType(manufacturer=1, model="ceos", slug="ceos")]

DEVICE_ROLES = [
    NetBoxDeviceRoles(
        name="dc-spine", slug="dc-spine", color="05195c", description="dc spine switches"
    ),
    NetBoxDeviceRoles(
        name="dc-leaf", slug="dc-leaf", color="0531e1", description="dc leaf switches"
    ),
]

REGIONS = [NetBoxRegions(name="demoland", slug="demoland")]

SITES = [NetBoxSites(name="demoville", slug="demoville", status="active", region=1)]

LOCATIONS = [NetBoxLocations(name="demoville-a", slug="demoville-a", site=1)]

DEVICES = []
for d in ("spine1", "spine2", "leaf1", "leaf2"):
    tag = "dc-even"
    if int(re.search(pattern=r"\d+$", string=d).group()) % 2 == 0:  # type: ignore
        tag = "dc-odd"

    DEVICES.append(
        NetBoxDevices(
            name=d,
            device_type=1,
            device_role=1,
            manufacturer=1,
            site=1,
            location=1,
            tags=[{"name": tag, "slug": tag}],
        )
    )

INTERFACES = []
for device_id, _ in enumerate(DEVICES, start=1):
    for intf in ("management0", "loopback0", "ethernet1", "ethernet2"):
        mgmt_only = True if intf.startswith("management") else False
        INTERFACES.append(NetBoxInterfaces(device=device_id, name=intf, mgmt_only=mgmt_only))

IP_ADDRESSES = [
    NetBoxIpAddresses(
        address="172.20.0.11",
        assigned_object_id=1,
        description="demoland/demoville/demoville-a::spine1::management0",
        tags=[{"name": "management-interface-ip", "slug": "management-interface-ip"}],
    ),
    NetBoxIpAddresses(
        address="10.255.255.11",
        assigned_object_id=2,
        description="demoland/demoville/demoville-a::spine1::loopback0",
        tags=[{"name": "management-interface-ip", "slug": "management-interface-ip"}],
        role="loopback",
    ),
    NetBoxIpAddresses(
        address="10.255.251.0",
        assigned_object_id=3,
        description="demoland/demoville/demoville-a::spine1::ethernet1",
        tags=[],
    ),
    NetBoxIpAddresses(
        address="10.255.251.2",
        assigned_object_id=4,
        description="demoland/demoville/demoville-a::spine1::ethernet2",
        tags=[],
    ),
    NetBoxIpAddresses(
        address="172.20.0.12",
        assigned_object_id=5,
        description="demoland/demoville/demoville-a::spine2::management0",
        tags=[{"name": "management-interface-ip", "slug": "management-interface-ip"}],
    ),
    NetBoxIpAddresses(
        address="10.255.255.12",
        assigned_object_id=6,
        description="demoland/demoville/demoville-a::spine2::loopback0",
        tags=[{"name": "management-interface-ip", "slug": "management-interface-ip"}],
        role="loopback",
    ),
    NetBoxIpAddresses(
        address="10.255.252.0",
        assigned_object_id=7,
        description="demoland/demoville/demoville-a::spine2::ethernet1",
        tags=[],
    ),
    NetBoxIpAddresses(
        address="10.255.252.2",
        assigned_object_id=8,
        description="demoland/demoville/demoville-a::spine2::ethernet2",
        tags=[],
    ),
    NetBoxIpAddresses(
        address="172.20.0.21",
        assigned_object_id=9,
        description="demoland/demoville/demoville-a::leaf1::management0",
        tags=[{"name": "management-interface-ip", "slug": "management-interface-ip"}],
    ),
    NetBoxIpAddresses(
        address="10.255.255.21",
        assigned_object_id=10,
        description="demoland/demoville/demoville-a::leaf1::loopback0",
        tags=[{"name": "management-interface-ip", "slug": "management-interface-ip"}],
        role="loopback",
    ),
    NetBoxIpAddresses(
        address="10.255.251.1",
        assigned_object_id=11,
        description="demoland/demoville/demoville-a::leaf1::ethernet1",
        tags=[],
    ),
    NetBoxIpAddresses(
        address="10.255.252.1",
        assigned_object_id=12,
        description="demoland/demoville/demoville-a::leaf1::ethernet2",
        tags=[],
    ),
    NetBoxIpAddresses(
        address="172.20.0.22",
        assigned_object_id=13,
        description="demoland/demoville/demoville-a::leaf2::management0",
        tags=[{"name": "management-interface-ip", "slug": "management-interface-ip"}],
    ),
    NetBoxIpAddresses(
        address="10.255.255.22",
        assigned_object_id=14,
        description="demoland/demoville/demoville-a::leaf2::loopback0",
        tags=[{"name": "management-interface-ip", "slug": "management-interface-ip"}],
        role="loopback",
    ),
    NetBoxIpAddresses(
        address="10.255.251.3",
        assigned_object_id=15,
        description="demoland/demoville/demoville-a::leaf2::ethernet1",
        tags=[],
    ),
    NetBoxIpAddresses(
        address="10.255.252.3",
        assigned_object_id=16,
        description="demoland/demoville/demoville-a::leaf2::ethernet2",
        tags=[],
    ),
]


CABLES = [
    NetBoxCables(termination_a_id=3, termination_b_id=11),
    NetBoxCables(termination_a_id=4, termination_b_id=15),
    NetBoxCables(termination_a_id=7, termination_b_id=12),
    NetBoxCables(termination_a_id=8, termination_b_id=16),
]

WEBHOOKS = [
    NetBoxWebHooks(
        name="jenkins-demo",
        payload_url="ttp://172.20.0.100:8080/generic-webhook-trigger/invok",
        content_types=["dcim.interface"],
        additional_headers="token: cool_token",
    )
]

OBJ_TO_ENDPOINT_MAP = {
    NetBoxTag: "/extras/tags/",
    NetBoxManufacturer: "/dcim/manufacturers/",
    NetBoxDeviceType: "/dcim/device-types/",
    NetBoxDeviceRoles: "/dcim/device-roles/",
    NetBoxRegions: "/dcim/regions/",
    NetBoxSites: "/dcim/sites/",
    NetBoxLocations: "/dcim/locations/",
    NetBoxDevices: "/dcim/devices/",
    NetBoxInterfaces: "/dcim/interfaces/",
    NetBoxIpAddresses: "/ipam/ip-addresses/",
    NetBoxCables: "/dcim/cables/",
    NetBoxWebHooks: "/extras/webhooks/",
}

seed_one = [TAGS, MANUFACTURERS, DEVICE_ROLES, REGIONS, WEBHOOKS]
seed_two = [DEVICE_TYPES, SITES]
seed_three = [LOCATIONS]
seed_four = [DEVICES]
seed_five = [INTERFACES]
seed_six = [CABLES, IP_ADDRESSES]
SEED = [seed_one, seed_two, seed_three, seed_four, seed_five]


async def create_objects(objects: List[IsDataclass]) -> None:
    """
    Create objects in netbox

    Args:
        objects:

    Returns:
        N/A

    Raises:
        Exception: if cant map object type to api endpoint
        Exception: if object already exists

    """
    if not objects:
        return

    endpoint = OBJ_TO_ENDPOINT_MAP.get(type(objects[0]))

    if not endpoint:
        raise Exception(f"cant determine endpoint for object type: {type(objects[0])}")

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{NETBOX_HOST_LOCALHOST}/api/{endpoint}",
            headers={"Authorization": f"Token {NETBOX_TOKEN}"},
            json=[asdict(o) for o in objects],
        )

    if resp.status_code != 201:
        raise Exception(
            "failed to push object(s), this script should only be used to *seed* netbox, "
            f"meaning that it expects there to be nothing in netbox to start! error: {resp.text}"
        )


async def main() -> None:
    """
    Seed data into netbox

    Args:
        N/A:

    Returns:
        N/A

    Raises:
        N/A

    """
    for seed_objs in SEED:
        await asyncio.gather(*[create_objects(objects=obj) for obj in seed_objs])  # type: ignore


if __name__ == "__main__":
    asyncio.run(main())
