# flask_app.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from api_class import APIClass

# Initialize Flask app
app = Flask(__name__)

# Create an instance of the API class
api_instance = APIClass()

@app.route('/api/status', methods=['GET'])
def get_status():
    """
    A simple GET endpoint to check the status of the API and the connection to Metasploit.
    """
    status = api_instance.get_status()
    return jsonify(status), 200

@app.route('/api/connect', methods=['POST'])
def connect_to_metasploit():
    """
    POST endpoint to establish a connection to Metasploit.
    """
    result = api_instance.connect_to_metasploit()
    return jsonify(result), 200

@app.route('/api/command', methods=['POST'])
def execute_command():
    """
    POST endpoint to execute a command on Metasploit.
    Expects JSON data with the command to be executed.
    """
    data = request.json  # Get the JSON payload from the request
    if not data or "command" not in data:
        return jsonify({"error": "No command provided"}), 400

    command = data["command"]
    result = api_instance.execute_command(command)
    return jsonify(result), 200

if __name__ == '__main__':
    # Running Flask app
    app.run(host='0.0.0.0', port=5000)
