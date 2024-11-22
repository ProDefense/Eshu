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

# Retrieve and print hosts
print("Getting Hosts")
hostSet = e.get_hosts()  # Retrieve all connected hosts across frameworks
print("Hosts =", hostSet)

# Only execute if "msf1" is available
if hostSet:
    try:
        print("Testing command execution...")
        commands = ["whoami", "uname -a"]
        host_details = {"id": "msf1", "os": "linux"}
        command_response = e.run_cmd(commands=commands, **host_details)
        print("Command response:", command_response)
    except ValueError as ve:
        print("Error during command execution:", ve)
else:
    print("No hosts available for command execution.")

# Task 3: List all exploit
# # List all exploit modules using the Metasploit instance / Looking for certain exploit
# exploits = msfInstance.list_exploit('exploits')  
# print(f"Available exploits: {len(exploits)}")
# for i, exploit in enumerate(exploits, start=1):
#     print(f" {i}. {exploit['fullname']}")