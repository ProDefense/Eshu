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
        self.config_path = os.path.join('operator1_localhost.cfg')
        asyncio.run(self.connect_to_sliver_server())

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
        sessions = await client.sessions()
        if not len(sessions):
            print("No Sliver Sessions!")
            return
        
        print ('Sessions: %r' % sessions)
        return sessions

    def send_cmd(self, hostID=None, os=None, commands=[]):
        """
        Run commands on the specified host ID.
        :param hostID: Unique host identifier (e.g., "sliver1").
        :param os: Operating system to filter the host.
        :param commands: List of commands to execute.
        :return: List of command outputs.
        """
        output = []
        if not hostID:
            raise ValueError("Host ID must be provided.")

        # Get agent details from targets mapping
        agent = self.targets.get(hostID)
        if not agent:
            raise ValueError(f"Host ID {hostID} not found in targets.")

        # Check OS if provided
        if os and agent["os"] != os:
            raise ValueError(f"Agent {agent['id']} is not running on the specified OS: {os}.")

        # Execute commands
        for cmd in commands:
            try:
                print(f"Sending command '{cmd}' to target with ID: {hostID}")
                response = self.client.execute(agent["id"], cmd)  # Replace with correct API call
                output.append(response.output)
                print("Command executed successfully.")
            except Exception as e:
                output.append(f"Error executing command '{cmd}': {e}")

        return output
