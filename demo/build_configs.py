import sys
from scrapli import AsyncScrapli

# Set to False if running locally, True if running in the container
DOCKER = True

def main():

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
    print("loading configs")

if __name__ == "__main__":
    try:
        test = sys.argv[1]
    except IndexError:
        test = None
    
    if test:
        print("hello world!")
        sys.exit(0)

    main()