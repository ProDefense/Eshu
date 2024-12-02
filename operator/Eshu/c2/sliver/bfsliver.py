import os
import time
import json
from sliver import SliverClient

class Sliver:
    def __init__(self, host=None, port=None, token=None):
        self.name = "Sliver API"
        print(f"Starting {self.name}")

        # Use environment variables if not passed in
        self.host = host or os.getenv('SLIVER_HOST', '127.0.0.1')
        self.port = port or int(os.getenv('SLIVER_PORT', 31337))
        self.token = token or os.getenv('SLIVER_TOKEN', None)

        config = {'host': self.host, 'port': self.port, 'token': self.token}
        
        try:
            self.client = SliverClient(config)
            print(f"Connected to Sliver server at {self.host}:{self.port}")
        except Exception as e:
            print(f"Error connecting to Sliver server: {e}")
            self.client = None
        self.targets = {}

    def save_session(self, framework_name, agent):
        """
        Save full agent details to self.targets.
        :param framework_name: Framework identifier (e.g., "sliver").
        :param agent: Full agent details (dictionary or object).
        """
        hostID = f"{framework_name}{agent['id']}"  # Ensure `agent` has an 'id' key
        self.targets[hostID] = agent

    def query_hosts(self):
        """
        Retrieve all agents from Sliver and map them to `self.targets`.
        :return: List of agent details.
        """
        hosts = []
        try:
            agents = self.client.get_agents()  # Replace with the correct Sliver API method
            print("Retrieving active agents in Sliver...")
            for agent in agents:
                # Map agent details to targets
                host_info = {
                    "id": agent["id"],  # Adjust based on the actual structure of `agent`
                    "name": agent["name"],
                    "os": agent["os"],
                    "platform": agent["platform"],
                    "last_seen": agent["last_seen"],
                }
                self.save_session("sliver", host_info)
                hosts.append(host_info)
        except AttributeError as e:
            print(f"Error querying hosts in Sliver: {e}")
        return hosts

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
