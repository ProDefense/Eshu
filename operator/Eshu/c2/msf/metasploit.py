import os
import time  # Fix: Import time module
from pymetasploit3.msfrpc import MsfRpcClient  # Fix: Import MsfRpcClient properly

class Metasploit:
    def __init__(self, password, Eshu, server="127.0.0.1", port=1337):
        self.name = "Metasploit API"
        print(f"Starting {self.name}")
        while True:
            try:
                self.client = MsfRpcClient(password, server=server, port=port)  # Fix: Ensure this import works
                break
            except:
                print("[!] Failed. Trying again...")
                time.sleep(1)

        print(f"[+] Successfully connected to MSF Server!")
        self.eshu = Eshu

    def query_hosts(self):
        """Retrieve all active sessions from Metasploit."""
        hosts = []
        print("Retrieving active sessions in Metasploit...")
        for session_id, session in self.client.sessions.list.items():
            host_info = {
                "session_id": session_id,
                "target_host": session.get("tunnel_peer", "N/A"),
                "platform": session.get("platform", "N/A"),
                "via_exploit": session.get("via_exploit", "N/A"),
                "via_payload": session.get("via_payload", "N/A"),
            }
            hosts.append(host_info)
            # Save host info to Eshu's targets
            host_id = f"msf{session_id}"
            self.eshu.save_session(host_id, host_info)
        print("Active sessions retrieved:", hosts)
        return hosts

    def send_cmd(self, id=None, os=None, commands=[]):
        if not id:
            raise ValueError("Host ID must be provided.")

        # Retrieve the session information
        session_info = self.eshu.targets.get(id)  # Retrieve host info
        if not session_info:
            raise ValueError(f"Host ID {id} not found in targets.")

        session_id = session_info.get("session_id")  # Get session ID from host info
        if not session_id:
            raise ValueError(f"No session ID found for Host ID {id}.")

        # Retrieve the session from Metasploit
        session = self.client.sessions.list.get(str(session_id))
        if not session:
            raise ValueError(f"Session with ID {session_id} not found.")

        # Check OS compatibility if provided
        session_platform = session.get("platform", "N/A")
        if os and session_platform != os and session_platform != "N/A":
            raise ValueError(f"Session {session_id} is not running on the specified OS: {os}.")

        # Execute commands
        output = []
        for cmd in commands:
            try:
                print(f"Sending command '{cmd}' to target with ID: {id}")
                cmd_output = self.client.sessions.session(str(session_id)).run_with_output(cmd, end_strs=["$", "#", "\n"])
                output.append(cmd_output)
                print(f"Successfully executed command: {cmd}")
            except Exception as e:
                output.append(f"Error executing command '{cmd}': {e}")
        return output

