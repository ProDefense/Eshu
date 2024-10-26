from flask import Flask, jsonify
from api_class import APIClass

app = Flask(__name__)
api_instance = APIClass()

@app.route('/api/status', methods=['GET'])
def get_status():
    status = api_instance.get_status()
    return jsonify(status), 200

@app.route('/api/connect', methods=['POST'])
def connect_to_metasploit():
    result = api_instance.connect_to_metasploit()
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
