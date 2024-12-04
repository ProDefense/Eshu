class BaseC2:
    def __init__(self, name, eshu):
        """
        Initialize the C2 framework with a name and a reference to the Eshu module.
        """
        self.name = name
        self.eshu = eshu  # Reference to the Eshu module for session management

    def query_hosts(self):
        """
        Retrieve all active hosts managed by this C2 framework.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement query_hosts")

    def send_cmd(self, id, os, commands):
        """
        Send commands to a specific host managed by this C2 framework.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement send_cmd")

    def get_name(self):
        """
        Get the name of the C2 framework.
        """
        return self.name