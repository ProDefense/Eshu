import re
import asyncio
from .baseC2.base_C2 import BaseC2

class Eshu:
    def __init__(self):
        self.name = "Eshu"
        print(f"Initializing {self.name}")
        self.c2s = {}  # Store registered C2 frameworks
        self.targets = {}  # Map hostID to full host details

    def save_session(self, session_name, host_info):
        """
        Save the session details to the `self.targets` dictionary.
        :param session_name: Unique session identifier (e.g., "msf1").
        :param host_info: Full host information (dictionary).
        """
        self.targets[session_name] = host_info

    def register(self, framework):
        """
        Register a C2 interface to be used.
        :param c2: Dictionary containing C2 name and framework instance.
        """
    
        if not hasattr(framework, '_NAME'):
          raise ValueError("Framework instance must have a '_NAME' attribute.")

        name = framework._NAME.lower()  # Normalize to lowercase for consistency
        print(f"[+] Registered {framework.__class__.__name__} with name '{name}'")
        self.c2s[name] = framework

    async def get_hosts(self, *frameworks):
        """
        Retrieve all host information from specified C2 frameworks.
        :param frameworks: Framework names to query (if empty, query all).
        :return: List of all host IDs across specified frameworks.
        """
        hosts = []
        print("Getting Hosts")
        frameworks = frameworks or self.c2s.keys()  # Query all C2 frameworks if none specified
        for framework in frameworks:
            try:
                framework_hosts = await self.c2s[framework].query_hosts()
                for host in framework_hosts:
                    session_id = host.get("session_id")
                    host_id = f"{framework}{session_id}"  # Generate unique host ID (e.g., "msf1")
                    if host_id not in self.targets:  # **Check for duplicates before saving**
                        self.save_session(host_id, host)  # Save to `self.targets` only if unique
                    hosts.append(host_id)  # Append the full host ID (e.g., "msf1")
                    
                print("[+] Hosts Stored")
            except Exception as e:
                print(f"[!] Error querying hosts in {framework}: {e}")
        return hosts

    def run_cmd(self, commands=None, id=None, os=None):
        """
        Run commands on a specific host.
        :param commands: List of commands to execute.
        :param id: Host ID (e.g., "msf1").
        :param os: Operating system of the target (optional).
        :return: Command outputs.
        """
        if not commands or not id:
            raise ValueError("[!] Both commands and host ID must be provided.")

        # Retrieve session info from Eshu's centralized data
        session_info = self.targets.get(id)
        if not session_info:
            raise ValueError(f"[!] No session information found for host ID {id}.")

        # Identify the C2 framework responsible for the host
        framework_name = self.getName(id)
        c2_framework = self.c2s.get(framework_name)
        if not c2_framework:
            raise ValueError(f"[!] Framework {framework_name} not registered.")

        # Pass the session data to the C2 framework for command execution
        session_id = session_info.get("session_id")
        outputs = c2_framework.send_cmd(session_id=session_id, os=os, commands=commands)
        
        print("[+] Command response(s):")
        for response in outputs:
            print(f"\t{response}")
        return outputs


    def getC2(self, hostID):
        """Extract the C2 framework (name) from hostID and return the corresponding C2."""
        name = self.getName(hostID)
        if name in self.c2s:
            print(f"[+] Found {name} instance")
            return self.c2s[name]
        else:
            raise ValueError(f"[!] No C2 found for framework {name}")

    def getName(self, hostID):
        """Extract the framework name from the hostID."""
        match = re.match(r"([a-zA-Z]+)", hostID)
        if match:
            return match.group(1)
        else:
            raise ValueError(f"[!] Invalid hostID format: {hostID}")
