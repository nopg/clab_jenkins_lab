#!/usr/bin/python3.7
"""launcher"""
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


class ClabLauncher:
    def __init__(self) -> None:
        """Dumb class to handling starting/stopping clab"""
        self.shutdown = False

        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum: Any, frame: Any) -> None:
        """
        Exit clab/container gracefully when SIGINT or SIGTERM recieved

        Args:
            signum: singum from the singal handler, unused here
            frame: frame from the signal handler, unused here

        Returns:
            N/A

        Raises:
            N/A

        """
        print(f"received exit signal {signum}; exiting")
        self.shutdown = True

    def start(self, reconfigure: bool = False) -> None:
        """
        Start clab

        Args:
            reconfigure: true/false add the reconfigure flag on deploy command

        Returns:
            N/A

        Raises:
            N/A

        """
        print("starting lab")

        launch_command = ["containerlab", "-t", "clab.yaml", "deploy"]
        if reconfigure is True:
            launch_command.append("--reconfigure")

        print(f"starting with command {launch_command}")

        proc = subprocess.run(launch_command, capture_output=True)

        if proc.returncode == 0:
            self.create_persistent_restart_log_dir()
            self.run()
        elif b"--reconfigure" in proc.stderr:
            self.start(reconfigure=True)
        else:
            print("failed launching...")
            print(f"stdout: {proc.stdout!r}")
            print(f"stderr: {proc.stderr!r}")
            print("stopping container...")
            self.shutdown = True

    def create_persistent_restart_log_dir(self) -> None:
        """
        Create the "persistentRestartLog" directoroy for cEOS instances

        For whatever reason this directory doesnt get created and it prevents cEOS from
        booting... so we simply wait for the flash dir to get mounted then go in
        and create that directory for EOS, then it boots nicely!

        Args:
            N/A

        Returns:
            N/A

        Raises:
            N/A

        """
        time.sleep(10)
        clab_dir = Path("./rg-clab-demo")

        for d in clab_dir.glob("*"):
            if Path(f"{d}/flash/persist").is_dir():
                Path(f"{d}/flash/persist/persistentRestartLog").mkdir(exist_ok=True)

    def run(self) -> None:
        """
        Run while the container has not received SIGINT or SIGTERM

        Once `self.shutdown` is set to True we'll stop sleeping and shut down clab

        Args:
            N/A

        Returns:
            N/A

        Raises:
            N/A

        """
        while self.shutdown is False:
            time.sleep(1)

        self.stop()

    def stop(self) -> None:
        """
        Stop clab

        Args:
            N/A

        Returns:
            N/A

        Raises:
            N/A

        """
        print("stopping lab")
        subprocess.run(["containerlab", "-t", "clab.yaml", "destroy", "--cleanup"])


if __name__ == "__main__":
    clab = ClabLauncher()
    clab.start()
    sys.exit(0)
