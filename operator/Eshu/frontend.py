import re

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

    def register(self, **c2):
        """
        Register a C2 interface to be used.
        :param c2: Dictionary containing C2 name and framework instance.
        """
        print(f"[+] Registered {c2['framework']} for {c2['name']}")
        self.c2s[c2['name']] = c2['framework']

    def get_hosts(self, *frameworks):
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
                framework_hosts = self.c2s[framework].query_hosts()  # Get hosts from the framework
                for host in framework_hosts:
                    session_id = host.get("session_id")
                    host_id = f"{framework}{session_id}"  # Generate unique host ID (e.g., "msf1")
                    self.save_session(host_id, host)  # Save to self.targets
                    hosts.append(host_id)  # Append the full host ID (e.g., "msf1")
                print("[+] Hosts Stored")
            except Exception as e:
                print(f"[!] Error querying hosts in {framework}: {e}")
        return hosts

    def run_cmd(self, commands=None, **hosts):
        """
        Run a command on specified host, agnostic of the underlying framework.
        :param commands: List of commands to execute.
        :param hosts: Host details, including 'id' and 'os'.
        :return: Command outputs.
        """
        if not commands:
            raise ValueError("[!] Commands must be provided to execute.")

        # Retrieve the corresponding C2 framework based on host ID
        c2 = self.getC2(hosts["id"])

        # Extract the session ID from the host info in `self.targets`
        session_info = self.targets.get(hosts["id"])
        if not session_info:
            raise ValueError(f"[!] No host found with ID {hosts['id']}")

        session_id = session_info.get("session_id")  # Ensure we extract the session ID correctly
        if not session_id:
            raise ValueError(f"[!] No session ID found for host ID {hosts['id']}")

        # Forward the command execution to the appropriate C2
        outputs = c2.send_cmd(id=hosts["id"], os=hosts.get("os", None), commands=commands)
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
