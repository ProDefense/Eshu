import Eshu
from Eshu.c2 import msf, sliver

#Initialize the Eshu library instance
e = Eshu.Eshu()

#Start the backend
Eshu.c2.Backend()

#Set up Metasploit and Sliver Instance
password = "memes"
msfInstance = msf.Metasploit(password)
sliverInstance = sliver.Sliver()

#Register  the C2 framework with Eshu centralized management
e.register(name=msf, framework=msfInstance)
e.register(name=sliver, framework=sliverInstance)

# Test 1: Query hosts in Metasploit
hosts = msfInstance.query_hosts()

# Test 2: Execute a command in an active Metasploit session
try:
    print("[+] Testing command execution in Metasploit session...")
    # Pass the commands as separate arguments in the correct format
    command_response = msfInstance.send_cmd(id="msf1", os="linux", commands=["whoami", "uname -a"])
    print("[+] Command response:", command_response)
except ValueError as ve:
    print("[-] Error during command execution:", ve)  

# Task 3: List all exploit
# # List all exploit modules using the Metasploit instance / Looking for certain exploit
# exploits = msfInstance.list_exploit('exploits')  
# print(f"Available exploits: {len(exploits)}")
# for i, exploit in enumerate(exploits, start=1):
#     print(f" {i}. {exploit['fullname']}")

