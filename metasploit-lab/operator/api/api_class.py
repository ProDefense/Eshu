# api_class.py

import msgpack
import http.client

class APIClass:
    def __init__(self, host='127.0.0.1', port=55553, username='msf', password='password'):
        """
        Initializes the API class to connect to Metasploit's RPC server.
        Update the host, port, username, and password as needed.
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.token = None
        self.connected = False

    def connect_to_metasploit(self):
        """
        Authenticates with the Metasploit RPC server and retrieves an auth token.
        """
        try:
            conn = http.client.HTTPConnection(self.host, self.port)
            payload = msgpack.packb({"method": "auth.login", "username": self.username, "password": self.password})
            headers = {'Content-Type': 'application/x-msgpack'}
            conn.request("POST", "/api", payload, headers)

            response = conn.getresponse()
            data = msgpack.unpackb(response.read())

            if data.get(b'result') == b'success':
                self.token = data[b'token'].decode()
                self.connected = True
                return {"message": "Connected to Metasploit", "token": self.token}
            else:
                return {"error": "Failed to connect to Metasploit", "details": data}

        except Exception as e:
            return {"error": str(e)}

    def execute_command(self, method, params=None):
        """
        Executes a command on Metasploit using the provided RPC method and parameters.
        """
        if not self.connected:
            return {"error": "Not connected to Metasploit"}

        if params is None:
            params = {}

        params["token"] = self.token
        payload = msgpack.packb({"method": method, **params})

        conn = http.client.HTTPConnection(self.host, self.port)
        headers = {'Content-Type': 'application/x-msgpack'}
        conn.request("POST", "/api", payload, headers)

        response = conn.getresponse()
        data = msgpack.unpackb(response.read())
        return data

    def get_status(self):
        """
        Returns the status of the API and connection.
        """
        return {
            "status": "API is running",
            "metasploit_connected": self.connected
        }
