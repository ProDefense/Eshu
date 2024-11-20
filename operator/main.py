import Eshu
from Eshu.c2 import msf, sliver

# Initialize Eshu and Backend
e = Eshu.Eshu()
Eshu.c2.Backend()

# Set up Metasploit and Sliver instances
password = "memes"
msfInstance = msf.Metasploit(password)
sliverInstance = sliver.Sliver()

# Register Metasploit and Sliver with Eshu
e.register(name=msf, framework=msfInstance)
e.register(name=sliver, framework=sliverInstance)

# Test 1: Query hosts in Metasploit
print("Testing host query in Metasploit...")
hosts = msfInstance.query_hosts()
print("Retrieved hosts:", hosts)

# Test 2: Execute a command in an active Metasploit session
try:
    print("Testing command execution in Metasploit session...")
    # Pass the commands as separate arguments in the correct format
    command_response = msfInstance.send_cmd(id="msf1", os="linux", commands=["whoami", "uname -a"])
    print("Command response:", command_response)
except ValueError as ve:
    print("Error during command execution:", ve)    