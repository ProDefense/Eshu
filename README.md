# Eshu Python Library v1

Common Language Platform for multiple Command and Control Frameworks

## Testing Lab Setup

This is an environment using Docker with test targets to
test using the ESHU CLP Python Library.

### To Simply Start...

Start Daemonized services

```console
docker compose up -d --build
```

Then launch into the operator machine
```console
# In one terminal
docker exec -it operator /bin/bash
```

To test successful library status
```bash
# Run main.py
cd eshuCLP
python3 main.py
```

To test successful network status
```bash
# Ping metasploitable2 @ 10.1.1.3
ping 10.1.1.3
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