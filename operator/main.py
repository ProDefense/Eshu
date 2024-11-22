import Eshu
from Eshu.c2 import msf, sliver

# Initialize Eshu and Backend
e = Eshu.Eshu()
Eshu.c2.Backend()

# Set up Metasploit and Sliver instances
password = "memes"
msfInstance = msf.Metasploit(password, e)
sliverInstance = sliver.Sliver()

# Register Metasploit and Sliver with Eshu
e.register(name="msf", framework=msfInstance)
e.register(name="sliver", framework=sliverInstance)

print("Getting Hosts")
hostSet = e.get_hosts("msf")
print("Hosts = ", hostSet)

## Test 1: Query hosts in Metasploit
#print("Testing host query in Metasploit...")
#hosts = msfInstance.query_hosts()
#print("Retrieved hosts:", hosts)
#
## Test 2: Unified run_cmd functionality
#try:
#    print("Testing command execution...")
#    commands = ["whoami", "uname -a"]
#    host_details = {"id": "msf1", "os": "linux"}
#    command_response = e.run_cmd(commands=commands, **host_details)
#    print("Command response:", command_response)
#except ValueError as ve:
#    print("Error during command execution:", ve)
