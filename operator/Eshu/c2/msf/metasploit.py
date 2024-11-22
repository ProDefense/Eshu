import os
import time
from pymetasploit3.msfrpc import MsfRpcClient

class Metasploit:
    def __init__(self, password, Eshu, server='127.0.0.1', port=1337):
        self.name = "Metasploit API"
        print(f"Starting {self.name}")
        while True:
            try:
                self.client = MsfRpcClient(password, server=server, port=port)
                break
            except:
                print("[!] Failed. Trying again...")
                time.sleep(1)

        print(f"[+] Successfully connected to MSF Server!")
        self.eshu = Eshu

    def query_hosts(self):
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
            self.eshu.save_session(f"msf{int(session_id)}", host_info)
        print("Active sessions retrieved:", hosts)
        return hosts

    def send_cmd(self, id=None, os=None, commands=[]):
        if not id:
            raise ValueError("Host ID must be provided.")
        session_id = self.eshu.targets.get(id) #FIRST THING, GET ACTUAL INT
        if not session_id:
            raise ValueError(f"Host ID {id} not found in targets.")
        session = self.client.sessions.list.get(str(session_id))
        if not session:
            raise ValueError(f"Session with ID {session_id} not found.")
        session_platform = session.get('platform', 'N/A')
        if os and session_platform != os and session_platform != 'N/A':
            raise ValueError(f"Session {session_id} is not running on the specified OS: {os}.")
        output = []
        for cmd in commands:
            try:
                print(f"Sent command {cmd} on target with id: {id}")
                cmd_output = self.client.sessions.session(str(session_id)).run_with_output(cmd, end_strs=["$", "#", "\n"])
                output.append(cmd_output)
                print(f"Successfully sent command, received output.")
            except Exception as e:
                output.append(f"Error executing command '{cmd}': {e}")
        return output
