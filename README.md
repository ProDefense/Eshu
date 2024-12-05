# Eshu Python Library v4

Common Language Platform for multiple Command and Control Frameworks

## Testing Lab Setup
This is an environment using Docker with test targets to
demonstrate using the Eshu CLP Python Library.

### To Simply Start...
Start Daemonized services

```console
docker compose up -d --build
```

Then launch into the operator machine in one terminal
```console
docker exec -it operator /bin/bash
```

To test network connection to vulnerable machine(VM)
```bash
ping 10.1.1.3
nmap -l metasploitable2
```

#### Firstly, testing Metasploit with main.py
In the terminal
```bash
python eshuCLP/main.py
```

#### Secondly, testing Sliver with server/client instances
In the same terminal
```bash
sliver-server
```
This launches the sliver server. In sliver server console
```console
new-operator --name operator1 --lhost localhost
multiplayer
```

In a second terminal launch into the operator machine
```console
docker exec -it operator /bin/bash
```
Then in operator's bash terminal
```bash
sliver-client import /workspace/operator1_localhost.cfg
sliver-client
```

Check on server side to see "operator1 has joined the game"

#### Clean Up
To stop all running containers
```console
docker compose stop
```

If stopped, start again with
```console
docker-compose start
```

To kill and remove all the running containers
```console
docker compose down
```