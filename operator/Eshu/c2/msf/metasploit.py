import os
import time  # Fix: Import time module
import json
import subprocess
from pymetasploit3.msfrpc import MsfRpcClient  # Fix: Import MsfRpcClient properly
from ...baseC2.base_C2 import BaseC2


class Metasploit(BaseC2):
     
    def __init__(self, password, server="127.0.0.1", port=1337):
        self.name = "Metasploit API"
        self.client = None
        self.server = server
        self.port = port
        self.password = password
        self.sessions = {}  # Store sessions locally within Metasploit
        self.start_msfconsole_with_script("/usr/src/metasploit-framework/docker/msfconsole.rc")
        self.connect_to_msfserver()

    def connect_to_msfserver(self):
        """Connect to the MSF server."""
        while True:
            try:
                self.client = MsfRpcClient(self.password, server=self.server, port=self.port)
                print("[+] Successfully connected to MSF Server!")
                break
            except Exception as e:
                print(f"[!] Failed to connect to MSF Server, RETRYING")
                time.sleep(0.5)

    def start_msfconsole_with_script(self, resource_script):
        """Start msfconsole with the specified resource script."""
        if not os.path.exists(resource_script):
            print(f"[!] Resource script {resource_script} not found!")
            return
        
        print(f"[+] Starting msfconsole with resource script: {resource_script}")
        try:
            subprocess.Popen(
                ["msfconsole", "-r", resource_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            time.sleep(0.5)  # Allow time for msfconsole to initialize
            print(f"[+] msfconsole started successfully!")
        except Exception as e:
            print(f"[!] Error starting msfconsole: {e}")

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
            # self.eshu.save_session(host_id, host_info)
        if hosts:
            print("[+] Active sessions retrieved:")
            for host in hosts:
                print(f"\tSession ID {host['session_id']}: Target Host: {host['target_host']}, Platform: {host['platform']}")
        else:
            print("[!] No active sessions.")
        return hosts

    def send_cmd(self, session_id=None, os=None, commands=[]):
        """
        Execute commands on a specific session in Metasploit.
        :param session_id: Session ID for the target.
        :param os: Operating system of the target (optional).
        :param commands: List of commands to execute.
        :return: Command outputs.
        """
        if not session_id:
            raise ValueError("[!] Session ID must be provided.")

        # Retrieve the session from Metasploit
        session = self.client.sessions.list.get(str(session_id))
        if not session:
            raise ValueError(f"[!] Session with ID {session_id} not found.")

        # Check OS compatibility if provided
        session_platform = session.get("platform", "N/A")
        if os and session_platform != os and session_platform != "N/A":
            raise ValueError(f"[!] Session {session_id} is not running on the specified OS: {os}.")

        # Execute commands
        output = []
        for cmd in commands:
            try:
                print(f"Sending command '{cmd}' to session {session_id}")
                cmd_output = self.client.sessions.session(str(session_id)).run_with_output(cmd, end_strs=["$", "#", "\n"])
                output.append(f"Output for {cmd}: {cmd_output}")
            except Exception as e:
                output.append(f"[!] Error executing command '{cmd}': {e}")
        return output

    def list_exploit(self, module_type):
       if not self.client:
           raise ConnectionError("[!] Not connected")
       return self.client.modules.search(module_type)
    
    # LEAVE THIS OPTION
    #def run_exploit(self, mtype, mname):
#
    #    # print(f"Type = {mtype} , name = {mname}")
    #    exploit = self.client.modules.use(mtype, mname)
    #    # print(exploit.options)
    #    exploit["RHOSTS"] = '10.1.1.3/24'
    #    exploit["USERNAME"] = 'msfadmin'
    #    exploit["PASSWORD"] = 'msfadmin'
    #    exploit["THREADS"] = 5 
    #    print(f"Running exploit: {exploit} with 1 second scan...")
    #    result = exploit.execute()
    #    # print(result)
    #    time.sleep(1)  # Allow time for the scan to run
    #    
    #    
    #    if 'job_id' in result:
    #        print("[+] Scan Complete!")
    #        time.sleep(1)
    #    # break
    #    else:
    #        print("[!] Scan failed. Retrying...")