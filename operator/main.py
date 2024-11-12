import Eshu
from Eshu import frontend
from Eshu.c2 import msf, sliver, backend

frontend.Frontend()
backend.Backend()
msfInstance = msf.metasploit.Metasploit()
sliverInstance = sliver.bfsliver.Sliver()

