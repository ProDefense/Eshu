# api_class.py

from pymetasploit3.msfrpc import MsfRpcClient
import os

class APIClass:
    def __init__(self, host='127.0.0.1', port=55553, password='password'):
        """
        Initializes the API class to connect to Metasploit's RPC server using PyMetasploit3.
        """
        self.host = host
        self.port = port
        self.password = password
        self.client = None
        self.connected = False
        self.connect_to_metasploit()

    def connect_to_metasploit(self):
        """
        Authenticates with the Metasploit RPC server and establishes the client connection.
        """
        try:
            self.client = MsfRpcClient(
                self.password,
                server=self.host,
                port=int(self.port)
            )
            self.connected = True
            return {"message": "Connected to Metasploit"}
        except Exception as e:
            return {"error": f"Failed to connect to Metasploit: {str(e)}"}

    def get_sessions(self):
        """
        Retrieves a list of active sessions.
        """
        if not self.connected:
            return {"error": "Not connected to Metasploit"}
        
        sessions = self.client.sessions.list
        return {"sessions": sessions}

    def get_session_info(self, session_id):
        """
        Retrieves information about a specific session.
        """
        if not self.connected:
            return {"error": "Not connected to Metasploit"}
        
        session = self.client.sessions.list.get(session_id)
        if session:
            return session
        else:
            return {"error": f"No session found with ID {session_id}"}

    def execute_command_in_session(self, session_id, command):
        """
        Executes a command in a specific session.
        """
        if not self.connected:
            return {"error": "Not connected to Metasploit"}
        
        try:
            session = self.client.sessions.session(session_id)
            result = session.write(command)
            return {"output": result}
        except Exception as e:
            return {"error": str(e)}

    def get_status(self):
        """
        Returns the status of the API and connection.
        """
        return {
            "status": "API is running",
            "metasploit_connected": self.connected
        }
