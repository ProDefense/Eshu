# If containers are running:
    docker compose down --remove-orphans

# Build and Start All Containers (might have to run this multiple times to go through)
docker compose up -d --build

# Check the status of all containers to confirm they’re up:
docker ps

# Enter the operator container:
docker exec -it operator /bin/bash

# Create the files:
cd /home
echo "msfadmin" > /home/user_file.txt
echo "msfadmin" > /home/pass_file.txt

# Once inside, start msfconsole with the required configuration file:
msfconsole -r /usr/src/metasploit-framework/docker/msfconsole.rc

# In a separate terminal, check the logs for eshu to ensure the Flask app started successfully (make sure you're within the improvedOp directory):
docker logs eshu

# Look for a line like this to confirm it’s listening on 10.1.1.99:5000:
 * Running on http://10.1.1.99:5000

# Once eshu is confirmed to be running, go back to msfconsole and send a test request from your host machine:
curl -X POST http://10.1.1.99:5000/exploit

# You should see:
{"result":{"job_id":0,"uuid":"qy08pPssI1VqkNutZQBQ4fhi"},"status":"module executed successfully"}
msf6 > [*] SSH session 1 opened (10.1.1.2:45471 -> 10.1.1.3:22) at 2024-11-07 03:45:40 +0000

# You can interact with the active SSH session from msfconsole by running:
sessions -i 1