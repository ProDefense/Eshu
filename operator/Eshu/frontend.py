import re

class Eshu:
    def __init__(self):
        self.name = "Eshu"
        print(f"Initializing {self.name}")
        self.c2s = {}
        self.targets = {}
        
    def save_session(self, session_name, session_instance):
        hostID = f"session_name"
        self.targets[hostID] = session_instance

    def register(self, **c2):
        """Register a C2 interface to be used."""
        print(f"Registered {c2['framework']} for {c2['name']}")
        self.c2s[c2['name']] = c2['framework']

    # Retrieve all host information from the specified C2 frameworks
    def get_hosts(self, *frameworks):
        hosts = []
        for c2 in frameworks:
            hosts.extend(self.c2s[c2].query_hosts())
        return hosts

    # Unified run_cmd call for different C2 frameworks
    def run_cmd(self, commands=None, **hosts):
        """
        Run a command on specified host, agnostic of the underlying framework.
        :param commands: List of commands to execute
        :param hosts: Host details, including 'id' and 'os'
        """
        if not commands:
            raise ValueError("Commands must be provided to execute.")

        # Retrieve the corresponding C2 framework based on host ID
        c2 = self.getC2(hosts['id'])

        # Forward the command execution to the appropriate C2
        outputs = c2.send_cmd(id=hosts['id'], os=hosts.get('os', None), commands=commands)
        return outputs

    def getC2(self, hostID):
        """Extract the C2 framework (name) from hostID and return the corresponding C2."""
        name = self.getName(hostID)
        if name in self.c2s:
            print(f"Found {name} instance")
            return self.c2s[name]
        else:
            raise ValueError(f"No C2 found for framework {name}")

    def getName(self, hostID):
        """Extract the framework name from the hostID."""
        match = re.match(r'([a-zA-Z]+)', hostID)
        if match:
            return match.group(1)
        else:
            raise ValueError(f"Invalid hostID format: {hostID}")
