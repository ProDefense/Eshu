# Eshu

Common Language Platform for multiple Command and Control Frameworks

## Testing Lab Setup

This is an environment using Docker with test targets to 
test using the ESHU api. 

### To Simply Start...

Start Daemonized services

```console
docker compose up -d eshuapi metasploitable2
```

Then start non-daemonizable services
```console
# In one terminal
docker compose run -it attacker_msf

# In another (using simple op)
docker compose run -it simple_operator
```

Then testing...

```bash
# Test API, assuming endpoint "exploits"
curl http://10.1.1.99:5000/exploits

# Test if we can see all ports on metasploitable (assuming .3 is the IP)
nmap -p- --min-rate=4000 10.1.1.3
```

To Kill all the running containers

```console
docker compose down
```

### Starting the Environment (more individually)

#### Start the container for the C2. In this example, MSF Console

```console
docker compose up -it attacker_msf
```

This will drop into the MSF console interaction. It will initialize
the MSFRPC server as well for ESHU to interact with. This is done using
the environment parameters passed into the container at runtime in the
docker-compose file. These parameters are:

- RPCPORT
- RPCPASS

RPCSERVER would be whatever the IP address is set on the container in the
compose file. In the msf docker container it is `0.0.0.0` so it will listen
on all interfaces attatched to the container instead of a specific IP or
interface.

#### Begin ESHU

Non-Daemonized:

```console
docker compose up eshuapi
```

Daemonized:

```console
docker compose up -d eshuapi
```

To change what port the container service is listening on, you will want to
change the `ESHU_PORT` in the docker-compose.yml file. If you do change this
port, you should also change the exposed port under the same service line in 
the docker-compose.yml file. 

#### Testing API Interaction

To test the API interaction, you can either use the standard Operator container
made or use the `simple_operator` service in the docker-compose.yml file.

```console
docker compose run -it simple_operator
```

This will drop you into a minimal alpine-linux container with basic utilities:

- VIM
- Python
- Curl
- Wget
- Bash
- NMap

Which can be used to test APIs against ESHU:

```bash
curl http://10.1.1.99:5000/exploits
```

This is assuming we are serving at `10.1.1.99:5000` and have an endpoint API
called `exploits`. 