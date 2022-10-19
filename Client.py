import socket as mysoc
import hmac

import sys

def fileLineCount(path):
	with open(path) as fileIn:
		for index, element in enumerate(fileIn):
			pass
	
	val = index + 1
	return val


# Socket to AS server
try:
	as_soc = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
	print("[C]: Socket for RS created")
except mysoc.error as err:
	print('{} \n'.format("socket open error ", err))

#Socket to TLDS1
try:
	tlds1 = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
	print("[C]: Socket for TLDS1 created")
except mysoc.error as err:
	print('{} \n'.format("socket open error ", err))

#Socket to TLDS2
try:
	tlds2 = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
	print("[C]: Socket for TLDS1 created")
except mysoc.error as err:
	print('{} \n'.format("socket open error ", err))



#Port for AS
asPort = 50020

# Client Host/IP setup
clientHost = mysoc.gethostname()
print("[C]: Client name is: ", clientHost)
clientIP = mysoc.gethostbyname(mysoc.gethostname())
print("[C]: Client IP is: ", clientIP)

# connect to AS_SERVER
as_ip = mysoc.gethostbyname(mysoc.gethostname())
print(as_ip)
server_bindingAS = (as_ip, asPort)
as_soc.connect(server_bindingAS) # RS will be waiting for connection
print ("[C]:  Connected to AS Server")


#TextFiles
DNS_HNS_TXT = 'PROJ3-HNS.txt'
# Import from file
inPath = DNS_HNS_TXT
numLinesInFile = fileLineCount(inPath)
inFile = open(inPath, 'r')
print("Num Of Lines in HNS: " + str(numLinesInFile))


#Send number of lines to AS
as_soc.send(str(numLinesInFile).encode('utf-8'))
data_from_server = as_soc.recv(100)
msg = data_from_server.decode('utf-8')
print("[C < AS]: Response: " + msg)
# send num of lookups

#create a file to output the data
fileOut = open("Resolved.txt", "w")
tsConnected = False

tlds1Connected = False
tlds2Connected = False
while True:
	# Each iteration = one lookup in AS
	inLine = inFile.readline()
	if not inLine:
		break
	
	# Send line to RS
	inLine = inLine.strip('\n')
	splitList = inLine.split()
	#take the key [0] and the challange[1] and make the digest
	d1 = hmac.new(splitList[0].encode(), splitList[1].encode("utf-8"))
	digest = d1.hexdigest()
	challange = splitList[1].strip()
	
	#now send the challange string [1] and the dijest
	as_soc.send("Sending Challenge".encode('utf-8'))
	as_soc.recv(1024)
	
	as_soc.send(challange.encode('utf-8'))
	print("[C > RS] Line Sent: ["+challange +"]")
	as_soc.send(digest.encode('utf-8'))
	print("[C > RS] Line Sent: " + digest)


	data_from_server = as_soc.recv(1024)
	msg = data_from_server.decode('utf-8')
	print("[C < RS]: Response : " + msg)
	
	

	if msg == "TLDS1":
		if not tlds1Connected:
			tlds1Connected = True
			tlds1Port = 40000
			tlds1_ip = mysoc.gethostbyname("cpp.cs.rutgers.edu")  # FIXME CHANGE TO TLDS LOCATION
			
			print(tlds1_ip)
			server_bindingTLDS1 = (tlds1_ip, tlds1Port)
			tlds1.connect(server_bindingTLDS1)  # RS will be waiting for connection
			print("[C]:  Connected to TLDS1 Server")
		
		#Confirmation who this is
		msg = "ThisClient"
		print("[C > TLDS1]: sending this to TLDS1 " + str(msg))
		tlds1.send(msg.encode('utf-8'))
		bleh = tlds1.recv(1024)
		print("FROM TLDS! TO CLIENT: ", bleh.decode('utf-8'))
		#send the host name
		tlds1.send(splitList[2].encode('utf-8'))
		print("[C > TLDS1]: now send host " + str(splitList[2]))
		msgRecv = tlds1.recv(1024).decode('utf-8')
		print("[C < TLDS1]: recieved full value: " + str(msgRecv))
		
		strToFile = msgRecv + "\n"
		fileOut.write(strToFile)
	elif msg == "TLDS2":
		if not tlds2Connected:
			tlds2Connected = True
			tlds2Port = 40100
			tlds2_ip = mysoc.gethostbyname("java.cs.rutgers.edu")  # FIXME CHANGE TO TLDS LOCATION
			print(tlds2_ip)
			server_bindingTLDS = (tlds2_ip, tlds2Port)
			tlds2.connect(server_bindingTLDS)  # RS will be waiting for connection
			print("[C]:  Connected to TLDS2 Server")
	
		# Confirmation who this is
		msg = "ThisClient"
		print("[C > TLDS2]: sending this to TLDS2 " + str(msg))
		tlds2.send(msg.encode('utf-8'))
		bleh = tlds2.recv(1024)
		print("FROM TLDS! TO CLIENT: ", bleh.decode('utf-8'))
		# send the host name
		tlds2.send(splitList[2].encode('utf-8'))
		print("[C > TLDS1]: now send host " + str(splitList[2]))
		msgRecv = tlds2.recv(1024).decode('utf-8')
		print("[C < TLDS1]: recieved full value: " + str(msgRecv))
		
		strToFile = msgRecv + "\n"
		fileOut.write(strToFile)
	

	print("")


#do not uncomment below
#ts.send("Kill TS".encode('utf-8'))

as_soc.close()
#do not uncomment belo
#ts.close()




#print("Stuff ended")
#data_from_server = rs.recv(1024)
#print("[C]: Data received from RS server: [", data_from_server.decode('utf-8'), "]")
#data_from_server_decoded= data_from_server.decode('utf-8')







