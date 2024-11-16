import Eshu
from Eshu.c2 import msf, sliver

e = Eshu.Eshu()
Eshu.c2.Backend()
password = "memes"
msfInstance = msf.Metasploit(password)
sliverInstance = sliver.Sliver()

e.register(name=msf, framework=msfInstance)
e.register(name=sliver, framework=sliverInstance)
e.get_hosts(msf, sliver)