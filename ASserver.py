import socket as mysoc
import sys

def fileLineCount(path):
	with open(path) as fileIn:
		for index, element in enumerate(fileIn):
			pass
	
	val = index + 1
	return val


print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

# Socket with Client
try:
	ss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
	print("[RS]: Server socket created")
except mysoc.error as err:
	print('{} \n'.format("socket open error ", err))

#Socket bound to pre-determined value for client
server_binding = ('', 50020)
ss.bind(server_binding)
ss.listen(1)
rsHost = mysoc.gethostname()
print("[RS]: RSServer host name is: ", rsHost)
localhost_ip = (mysoc.gethostbyname(rsHost))
print("[RS]: RSServer IP address is  ", localhost_ip)
csockid, addr = ss.accept()
print("[RS]: Got a connection request from a client to RSSERVER", addr)


# TLDS1 Socket
try:
	TLDS1 = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
	print("[RS]: Socket for TS_COM created")
except mysoc.error as err:
	print('{} \n'.format("socket open error (TSLDS1)", err))

# TLDS2 SOCKET
try:
	TLDS2 = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
	print("[RS]: Socket for TS_EDU created")
except mysoc.error as err:
	print('{} \n'.format("TS socket open error ", err))



#FIXME will need to change when testing on different machine- not my host
TLDS1HostName = "cpp.cs.rutgers.edu" #65500
TLDS2HostName = "java.cs.rutgers.edu" #60000
TLDS1HostConnected = False
TLDS2HostConnected = False

data_from_client = csockid.recv(100)
msg = data_from_client.decode('utf-8')
print("[RS] Received Num of lookups: " + msg)
csockid.send("NumLookups received".encode('utf-8'))

while 1:
	print("=========== LOOKUP ==============")
	data_from_client = csockid.recv(1024)
	#data_from_client2 = csockid.recv(100)

	if not data_from_client:
		print("BREAKING");
		break
		
	msg = data_from_client.decode('utf-8')
	print(msg)
	if msg == "Sending Challenge":
		# send ack back
		csockid.send("Ready for Challenge".encode('utf-8'))
		data_from_client = csockid.recv(100)
		data_from_client2 = csockid.recv(100)
		
		challange = data_from_client.decode('utf-8')
		digest = data_from_client2.decode('utf-8')
		print("[RS] DNS received from Client Challenge:[" + challange)
		print("[RS] DNS received from Client Digest: " + digest)
		
		if not TLDS1HostConnected:
			TLDS1HostConnected = True
			TLDS1Port = 65500
			TLDS1_ip = mysoc.gethostbyname(TLDS1HostName)
			server_bindingTLDS1 = (TLDS1_ip, TLDS1Port)
			TLDS1.connect(server_bindingTLDS1)
			print("[C]: Connected to TLDS1 Server")
		if not TLDS2HostConnected:
			TLDS2HostConnected = True
			TLDS2Port = 60000
			TLDS2_ip = mysoc.gethostbyname(TLDS2HostName)
			server_bindingTLDS2 = (TLDS2_ip, TLDS2Port)
			TLDS2.connect(server_bindingTLDS2)
			print("[C]: Connected to TLDS2 Server")
		
		# send the hostname to both TLDS Servers 1
		
		print("[RS > TLDS1] sending: " + challange)
		TLDS1.send("Sending Challenge".encode('utf-8'))
		TLDS1.recv(1024)
		TLDS1.send(challange.encode('utf-8'))
		data_from_TLDS1 = TLDS1.recv(1024)
		print("[RS < TLDS1] received:  ", data_from_TLDS1.decode('utf-8'))
		msgTLDS1 = data_from_TLDS1.decode('utf-8')
		
		# send the hostname to both TLDS Servers 2
		print("[RS > TLDS2] sending: " + challange)
		TLDS2.send("Sending Challenge".encode('utf-8'))
		TLDS2.recv(1024)
		TLDS2.send(challange.encode('utf-8'))
		data_from_TLDS2 = TLDS2.recv(1024)
		print("[RS < TLDS2] received:  ", data_from_TLDS2.decode('utf-8'))
		msgTLDS2 = data_from_TLDS2.decode('utf-8')
		
		# which ever is a match we send the host name of that TLDS server
		if msgTLDS1 == digest:
			print("WE FOUND A MATH FROM TLDS1 BOIIIII");
			TLDS1.send("WaitForClient".encode('utf-8'))
			TLDS2.send("DoNotWait".encode('utf-8'))
			csockid.send("TLDS1".encode('utf-8'))
		elif msgTLDS2 == digest:
			print("TLDS2 BOIIIII BABYYYYY");
			TLDS1.send("DoNotWait".encode('utf-8'))
			TLDS2.send("WaitForClient".encode('utf-8'))
			csockid.send("TLDS2".encode('utf-8'))
		else:
			TLDS1.send("DoNotWait".encode('utf-8'))
			TLDS2.send("DoNotWait".encode('utf-8'))
			csockid.send("NOT FOUND IN ANY".encode('utf-8'))
	
	
	
	elif msg == "Terminate All":
		print()
		
	# 	if "com" in msg:
	# 		print("must connect to COM: ", msg)
	# 		if not COMHostConnected:
	# 			COMHostConnected = True
	# 			COMPort = 65500
	# 			com_ip = mysoc.gethostbyname(COMHostName)
	# 			#FIXME will change here for the ports on diff machines
	# 			server_bindingCOM = (com_ip, COMPort)
	# 			com.connect(server_bindingCOM)
	# 			print("[C]: Connected to COM Server")
	#
	# 		# send the hostname to com
	# 		print("[RS > COM] sending: " + msg)
	# 		com.send(msg.encode('utf-8'))
	# 		data_from_com = com.recv(1024)
	# 		print("[RS < COM] received:  ", data_from_com.decode('utf-8'))
	# 		msgCOM = data_from_com.decode('utf-8')
	# 		csockid.send(msgCOM.encode('utf-8'))
	# 	elif "edu" in msg:
	# 		print("must connect to EDU:  ", msg)
	# 		if not EDUHostConnected:
	# 			EDUHostConnected = True
	# 			EDUPort = 55000
	# 			edu_ip = mysoc.gethostbyname(EDUHostName)
	# 			# FIXME will change here for the ports on diff machines
	# 			server_bindingEDU = (edu_ip, EDUPort)
	# 			edu.connect(server_bindingEDU)
	# 			print("[C]: Connected to EDU Server")
	#
	# 		# send the hostname to com
	# 		print("[RS > EDU] sending: " + msg)
	# 		edu.send(msg.encode('utf-8'))
	# 		data_from_edu = edu.recv(1024)
	# 		print("[RS < EDU] received:  ", data_from_edu.decode('utf-8'))
	# 		msgEDU = data_from_edu.decode('utf-8')
	# 		csockid.send(msgEDU.encode('utf-8'))
	# 	else:
	# 		print("error:  ", msg)
	# 		strSendBack = "Error"
	# 		csockid.send(strSendBack.encode('utf-8'))
			
	# send back the original message or something saying not found
	# csockid.send(strNS.encode('utf-8'))
	#csockid.send('Sending back for test'.encode('utf-8'))

	
	print("")
	
#TLDS1.send("Kill COM".encode('utf-8'))
#TLDS2.send("Kill EDU".encode('utf-8'))

# Close the server socket
ss.close()
TLDS1.send("Terminate".encode('utf-8'))
TLDS1.close()
TLDS2.send("Terminate".encode('utf-8'))
TLDS2.close()
print("#### CLOSE RS SERVER")
exit()
