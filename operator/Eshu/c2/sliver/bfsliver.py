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

    def save_session(self, framework_name, agent_id):
        """Map framework and agent ID to a unique host ID."""
        hostID = f"{framework_name}{agent_id}"
        self.targets[hostID] = agent_id

    def query_hosts(self):
        """Retrieve all hosts from Sliver, filtered by kwargs."""
        if not self.client:
            raise ConnectionError("Sliver client is not connected.")
        hosts = self.client.list_agents()

        # Register new agents into the target's mapping
        for agent in hosts:
            if not any(agent.id == val for val in self.targets.values()):
                self.save_session("sliver", agent.id)
            return hosts

    def send_cmd(self, hostID=None, os=None, *commands):
        """
        Run commands on the host specified by `id`, filtered by OS if provided.
        """
        output = []
        if not hostID:
            raise ValueError("Host ID must be provided.")

        # Get agent ID from targets mapping
        agent_id = self.targets.get(hostID)
        if not agent_id:
            raise ValueError(f"Host ID {hostID} not found in targets.")

        # Locate the agent
        agent = next((a for a in self.client.list_agents() if a.id == agent_id), None)
        if not agent:
            raise ValueError(f"Agent with ID {agent_id} not found.")

        # Check OS/platform if provided
        if os and agent.os != os:
            raise ValueError(f"Agent {agent_id} is not running on the specified OS: {os}.")

        # Run the commands and collect output
        for cmd in commands:
            try:
                print(f"Sending command '{cmd}' to target with ID: {hostID}")
                response = self.client.execute(agent.id, cmd)
                output.append(response.output)
                print("Command executed successfully.")
            except Exception as e:
                output.append(f"Error executing command '{cmd}': {e}")

        return output