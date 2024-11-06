from flask import Flask, jsonify, request
from api_class import APIClass

app = Flask(__name__)
api_instance = APIClass()

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get the API and Metasploit connection status."""
    status = api_instance.get_status()
    return jsonify(status), 200

@app.route('/api/connect', methods=['POST'])
def connect_to_metasploit():
    """Connect to the Metasploit RPC server."""
    result = api_instance.connect_to_metasploit()
    return jsonify(result), 200

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    """List all active Metasploit sessions."""
    sessions = api_instance.get_sessions()
    return jsonify(sessions), 200

@app.route('/api/session/<int:session_id>', methods=['GET'])
def get_session_info(session_id):
    """Retrieve information for a specific session."""
    session_info = api_instance.get_session_info(session_id)
    return jsonify(session_info), 200

@app.route('/api/session/<int:session_id>/command', methods=['POST'])
def execute_command(session_id):
    """Execute a command in a specified session."""
    data = request.args  # Retrieve the command from URL parameters
    command = data.get('cmd')

    if not command:
        return jsonify({"error": "No command provided"}), 400

    result = api_instance.execute_command_in_session(session_id, command)
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
