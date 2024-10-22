from flask import Flask, jsonify,request
from api import API  # Assuming you have API defined in api/__init__.py


app = Flask(__name__)
eshu_api = API()

@app.route("/hosts", methods=["GET"])
def get_hosts():
    hosts = eshu_api.get_hosts()
    return jsonify({"hosts": hosts})

@app.route("/run", methods=["POST"])
def run_command():
    data = request.json
    command = data.get('command')
    result = eshu_api.run_command(command)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337)
