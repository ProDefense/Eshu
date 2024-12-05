# Eshu Python Library v3

Common Language Platform for multiple Command and Control Frameworks

## To Build and Start Sliver C2

Navigate to Sliver folder
```console
cd Sliver
```

Build Sliver image
```console
docker build -t sliver .
```

Start Sliver
```console
docker run --name sliver_container -it sliver
```

To stop
```console
sliver > exit
```

To start up container and enter Sliver again
```console
docker start sliver_container
docker exec -it sliver_container /opt/sliver-server
```

If you want to stop the container after exiting again
```console
docker stop sliver_container
```

## Testing Lab Setup

This is an environment using Docker with test targets to
demonstrate using the Eshu CLP Python Library.

### To Simply Start...

Start Daemonized services

```console
docker compose up -d --build
```

Then launch into the operator machine
```console
docker exec -it operator /bin/bash
```

In the terminal
```bash
python eshuCLP/main.py
```

To test network connection to vulnerable machine(VM)
```bash
ping 10.1.1.3
nmap -l metasploitable2
```

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