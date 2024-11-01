# api_class.py

from pymetasploit3.msfrpc import MsfRpcClient
import os

class APIClass:
    def __init__(self):
        """
        Initializes the API class to connect to Metasploit's RPC server using PyMetasploit3.
        """
        self.host = os.getenv("MSF_HOST", "127.0.0.1")
        self.port = int(os.getenv("MSF_PORT", 55553))
        self.password = os.getenv("MSF_PASSWORD", "password")
        self.client = None
        self.connected = False
        self.connect_to_metasploit()

    def connect_to_metasploit(self):
        try:
            self.client = MsfRpcClient(
                self.password,
                server=self.host,
                port=self.port
            )
            self.connected = True
            return {"message": "Connected to Metasploit"}
        except Exception as e:
            return {"error": f"Failed to connect to Metasploit: {str(e)}"}

    # Additional methods for session management as previously defined
