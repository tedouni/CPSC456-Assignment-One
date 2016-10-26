Tayseer Edouni
taedouni@gmail.com
CPSC 456


Attacking System:
VM1: 192.168.1.5
Default password: "123456"
All source files must be placed in the /tmp directory of the attacking system.  If the system reboots, the source files will be deleted, therefore, copies of them are on the attacking system's Desktop.


Replicator_worm:
This worm works correctly. 
1) cd to /tmp directory
2) python replicator_worm.py

Extorter_worm:
*NOTE* This worm deletes Document folder as requested.
This worm works correctly. The encrypted archive file is named "exdir.tar.enc" and is located in /home/ubuntu/
1) cd to /tmp directory
2) python extorter_worm.py

Passwordthief_worm:
This worm works correctly.
1) cd to /tmp directory
2) python passwordthief_worm.py
password files (from victim computers) will be located in /tmp of attacking system. 

