# Eshu Python Library v2

Common Language Platform for multiple Command and Control Frameworks

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
msfconsole -r /usr/src/metasploit-framework/docker/msfconsole.rc

use auxiliary/scanner/ssh/ssh_login
set RHOSTS 10.1.1.3
set USERNAME msfadmin
set PASSWORD msfadmin
run

cd eshuCLP
python main.py
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