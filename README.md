# Operator

Based on original and nathan, improvedOp will aim to act as a networked client that runs 
msfconsole and can throw exploits in preparation of using the API

```bash
# navigate to improvedop, then build
docker compose up -d --build

# independent
docker exec -it operator /bin/bash
```

#### Exploitation

To throw the exploit:
```bash
# launch metasploit
msfconsole
```


#### Post-Exploitation API Interaction

Once integrated with Eshu:
