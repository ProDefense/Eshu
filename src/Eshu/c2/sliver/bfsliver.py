import os
import asyncio
from sliver import SliverClient, SliverClientConfig
from ...baseC2.base_C2 import BaseC2

class Sliver(BaseC2):
    _NAME = "sliver" # C2 Name

    def __init__(self, host='127.0.0.1', port=31337, token=None):
        self.name = "Sliver API"
        self.client = None
        self.config = None
        self.beacons = None
        self.config_path = os.path.join('operator1_localhost.cfg')
    
    async def start(self): 
        await self.connect_to_sliver_server()

    async def connect_to_sliver_server(self):
        """Connect to the Sliver server."""
        print(f"=============== Starting {self.name} ===============")
        self.config = SliverClientConfig.parse_config_file(self.config_path)
        self.client = SliverClient(self.config)
        await self.client.connect()
        print("[+] Successfully connected to Sliver Server!")

    async def query_hosts(self):
        """
        Retrieve all agents from Sliver and map them to `self.targets`.
        In this case, this would be sessions
        :return: List of agent details.
        """

        hosts = []
        print("Retrieving active beacons in Sliver...")
        """Hosts in this case is a beacon, rather than a session"""
        self.beacons = await self.client.beacons()
        if not len(self.beacons):
            print('[!] No Sliver hosts!')
            return

        for beacon in self.beacons:
            host_info = {
                "session_id": beacon.ID,
                "target_host" : beacon.RemoteAddress,
                "platform" : beacon.OS
            }
            hosts.append(host_info)
            host_id = f"sliver{beacon.ID}"
        if hosts:
            print("[+] Active beacons retrieved:")
            for host in hosts:
                print(f"\tBeacon ID: {host['session_id']}, Target Host: {host['target_host']}, Platform: {host['platform']}")
        else:
            print("[!] No active beacons.")
        return hosts

    async def send_cmd(self, session_id=None, os=None, commands=[]):
        """
        Run commands on the specified host ID.
        :param hostID: Unique host identifier (e.g., "sliver1").
        :param os: Operating system to filter the host.
        :param commands: List of commands to execute.
        :return: List of command outputs.
        """
        output = []
        if not session_id:
            raise ValueError("Beacon ID must be provided.")

        # Find beacon with corresponding ID
        beacon = None
        for b in self.beacons:
            print(b.ID)
            if b.ID == session_id:
                beacon = b
                break
        if not beacon:
            raise ValueError(f"[!] Beacon with ID {session_id} not found.")

        # Check OS if provided
        if os and beacon.OS != os:
            raise ValueError(f"Agent {session_id} is not running on the specified OS: {os}.")

        # Execute commands
        for cmd in commands:
            try:
                print(f"Sending command '{cmd}' to target with ID: {session_id}")
                response_task = await self.beacon.execute(cmd)
                response = await response_task
                print("Command executed successfully.")
                print(response)
            except Exception as e:
                output.append(f"Error executing command '{cmd}': {e}")

        return output
