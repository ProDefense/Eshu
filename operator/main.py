import Eshu
from Eshu.c2 import msf, sliver

# Initialize Eshu Instance
e = Eshu.Eshu()

# Set up Metasploit and Sliver instances
password = "memes"
msfInstance = msf.Metasploit(password, e)
#sliverInstance = sliver.Sliver()

# Register Metasploit and Sliver with Eshu
e.register(name="msf", framework=msfInstance)
#e.register(name="sliver", framework=sliverInstance)

msfInstance.run_exploit('auxiliary', 'scanner/ssh/ssh_login')
# Retrieve and print hosts
hostSet = e.get_hosts()  # Retrieve all connected hosts across frameworks
print("Hosts =", hostSet)

# Only execute if hostSet is populated when querying "get_hosts"
if hostSet:
    try:
        print("Testing command execution...")
        commands = ["whoami", "uname -a"]
        host_details = {"id": "msf1", "os": "linux"}
        e.run_cmd(commands=commands, **host_details)
    except ValueError as ve:
        print("[!] Error during command execution:", ve)
else:
    print("[!] No hosts available for command execution.")

# Task 3: List all exploit
# # List all exploit modules using the Metasploit instance / Looking for certain exploit
# exploits = msfInstance.list_exploit('exploits')  
# print(f"Available exploits: {len(exploits)}")
# for i, exploit in enumerate(exploits, start=1):
#     print(f" {i}. {exploit['fullname']}")