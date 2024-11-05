# Operator

Based on original and nathan, improvedOp will aim to act as a networked client that runs 
msfconsole and can throw exploits in preparation of using the API

### System Set Up
```bash
# navigate to improvedop directory, then build
docker compose up -d --build

# access operator
docker exec -it operator /bin/bash
```

#### Exploitation

Necessary when launching Metasploit MSFConsole:
```bash
# launch metasploit
msfconsole -r /usr/src/metasploit-framework/docker/msfconsole.rc
```

#### Post-Exploitation API Interaction

Once integrated with Eshu, perform the following
