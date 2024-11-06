from pymetasploit3.msfrpc import MsfRpcClient
import os

class APIClass:
    def __init__(self):
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

    def get_sessions(self):
        """Retrieve a list of all active sessions."""
        if not self.connected:
            return {"error": "Not connected to Metasploit"}
        
        sessions = self.client.sessions.list
        return {"sessions": sessions}

    def get_session_info(self, session_id):
        """Retrieve information for a specific session."""
        if not self.connected:
            return {"error": "Not connected to Metasploit"}
        
        session = self.client.sessions.list.get(session_id)
        if session:
            return session
        else:
            return {"error": f"No session found with ID {session_id}"}

    def execute_command_in_session(self, session_id, command):
        """Execute a command in a specific session."""
        if not self.connected:
            return {"error": "Not connected to Metasploit"}
        
        try:
            session = self.client.sessions.session(session_id)
            result = session.write(command)
            return {"output": result}
        except Exception as e:
            return {"error": str(e)}

    def get_status(self):
        """Return the status of the API and connection."""
        return {
            "status": "API is running",
            "metasploit_connected": self.connected
        }
