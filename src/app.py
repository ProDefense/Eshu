from flask import Flask, jsonify, request
from pymetasploit3.msfrpc import MsfRpcClient
import os

app = Flask(__name__)

MSF_SERVER = os.getenv("MSF_HOST", "127.0.0.1")
MSF_PORT = os.getenv("MSF_PORT", 55553)
ESHU_PORT = int(os.getenv("ESHU_PORT", 5000))

# Load Metasploit server configuration from environment variables
print(f"[-] Attempting to connect to MSF at {MSF_SERVER}:{MSF_PORT}")
while True: # just keep attempting to load if its not started yet
    try: 
        client = MsfRpcClient(
            os.getenv("MSF_PASSWORD"),
            server=MSF_SERVER,
            port=int(MSF_PORT)
        )
        # Success! Breakout
        break
    except:
        print("[!] Failed. Trying again...")
        pass

print(f"[+] Successfully connected to MSF Server!")

@app.route('/exploits', methods=['GET'])
def list_exploits():
    """List all available exploits in Metasploit."""
    exploits = client.modules.exploits
    return jsonify(exploits)

@app.route('/exploit', methods=['POST'])
def run_exploit():
    """Run a specific exploit with given options."""
    data = request.json
    exploit = client.modules.use('exploit', data['exploit_name'])
    for key, value in data['options'].items():
        exploit[key] = value
    exploit.execute()
    return jsonify({"status": "exploit executed", "name": data['exploit_name']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=ESHU_PORT)
