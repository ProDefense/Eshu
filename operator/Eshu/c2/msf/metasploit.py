import os
import time
import json
import subprocess
from pymetasploit3.msfrpc import MsfRpcClient
class Metasploit:
    
    def __init__(self, password, server='127.0.0.1', port=1337):
        self.name = "Metasploit API"
        print(f"Starting {self.name}")
        self.start_msfconsole_with_script("/usr/src/metasploit-framework/docker/msfconsole.rc")
        while True:
            try: 
                self.client = MsfRpcClient(password, server=server, port=port)
                break  # Successful connection
            except:
                print("[!] Failed. Trying again...")
                time.sleep(1)

        print(f"[+] Successfully connected to MSF Server!")
        self.targets = {}

    def start_msfconsole_with_script(self, resource_script):
        """Start msfconsole with the specified resource script."""
        if not os.path.exists(resource_script):
            print(f"[-] Resource script {resource_script} not found!")
            return
        
        print(f"[+] Starting msfconsole with resource script: {resource_script}")
        try:
            subprocess.Popen(
                ["msfconsole", "-r", resource_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            time.sleep(5)  # Allow time for msfconsole to initialize
            print(f"[+] msfconsole started successfully!")
        except Exception as e:
            print(f"[!] Error starting msfconsole: {e}")

    def save_session(self, framework_name, session_id):
        hostID = f"{framework_name}{session_id}"
        self.targets[hostID] = session_id

    def save_session(self, framework_name, session_id):
        hostID = f"{framework_name}{session_id}"
        self.targets[hostID] = session_id

    def query_hosts(self):

        run_exploit = self.client.modules.use('auxiliary', 'scanner/ssh/ssh_login')
        run_exploit["RHOSTS"] = '10.1.1.3/24'
        run_exploit["USERNAME"] = 'msfadmin'
        run_exploit["PASSWORD"] = 'msfadmin'
        run_exploit["THREADS"] = 5 

        result = run_exploit.execute()
        time.sleep(100)  # Allow time for the scan to run

        if result.get("job_id"):
            print("[+] Scan Complete!")
        else:
            print("[!] Scan failed. Retrying...")

        hosts = []
        print("[+] Retrieving active sessions in Metasploit...")

        # Loop through active sessions to gather information
        for session_id, session in self.client.sessions.list.items():
            host_info = {
                "session_id": session_id,
                "target_host": session.get("tunnel_peer", "N/A"),
                "platform": session.get("platform", "N/A"),
                "via_exploit": session.get("via_exploit", "N/A"),
                "via_payload": session.get("via_payload", "N/A"),
            }
            hosts.append(host_info)
            # Save the session to targets with the format "msf<session_id>"
            self.save_session("msf", int(session_id))

        print("[+] Active sessions retrieved:")
        if hosts:
            for host in hosts:
                print(f"Session ID {host['session_id']}: Target Host: {host['target_host']}, Platform: {host['platform']}")
        else:
            print("[-] No active sessions.")

        return hosts


    def send_cmd(self, id=None, os=None, commands=[]):
        output = []
        if not id:
            raise ValueError("[+] Host ID must be provided.")

        # Get session ID from targets mapping
        session_id = self.targets.get(id)
        if not session_id:
            raise ValueError(f"[+] Host ID {id} not found in targets.")

        # Locate the session
        session = self.client.sessions.list.get(str(session_id))
        if not session:
            raise ValueError(f"[+] Session with ID {session_id} not found.")

        # Check OS/platform if provided, and skip check if platform is not available
        session_platform = session.get('platform', 'N/A')
        if os and session_platform != os and session_platform != 'N/A':
            raise ValueError(f"[+] Session {session_id} is not running on the specified OS: {os}. It is on platform: {session_platform}.")

        # Run the command and collect output
        for cmd in commands:
            try:
                print(f"[+] Sent command {cmd} on target with id: {id}")
                cmd_output = self.client.sessions.session(str(session_id)).run_with_output(cmd, end_strs=["$", "#", "\n"])
                output.append(cmd_output)
                print(f"[+] Successfully sent command, received output.")
            except Exception as e:
                output.append(f"[!] Error executing command '{cmd}': {e}")

        return output
    
    def list_exploit(self, module_type):
        if not self.client:
            raise ConnectionError("[-] Not connected")
        return self.client.modules.search(module_type)
    
    # def run_exploit(self, module_type, target_info = None):

    #     if not target_info:
    #         raise ValueError("[-] Target Information is required to run a scan")
        
    #     while True:
    #         #running exploit
    #         if module_type == 'auxiliary':
    #             print(module_name)
    #         elif module_type == 'exploit':
    #             print(module_name)
    #         elif module_type == 'post':
    #             print(module_name)
    #         elif module_type == 'nop':
    #             print(module_name)
    #         elif module_type == 'encoder':
    #             print(module_name)
    #         elif module_type == 'payload':
    #             print(module_name)
    #         else:
    #             raise ValueError(f"[-]  {module_type} is unknown module!")



