#***************************************
#	FileName: Constants.py
#
#	Description:
#	This file contains the constants used by
#	the rest of the program.
#
#****************************************

#Run using blacklist or whitelist
useBlackList = False

#The interface on which the progam will run
theInterface = "eth1"

#Channel
channel = "11"

#Essid
essid = "YOBATMAN"

#The type code for OGM packets
theOGMType = 0x3123 

#The type code for Message Packets
theMessageType = 0x3122

#The broadcast address
BROADCAST = "\xFF" * 6

#Time to live value for packets
ttl_value = 5

#Time between sending OGM packets
timeBetweenOGM = 3
#Note: There also could be up to 
maxRandomTimeBetweenOGM = 2
#seconds between OGM messages

#Verbose Mode ON/OFF
verbose = True

#Socket TimeOut
socketTimeout = 0
#if 0, the socket is non-blocking

#Sequence Number Start
sequenceNumberStart = 1000

#Recv Packet Size
packetSizeRecv = 2048

#Queue Size 
QueueSize = 0
#Here, 0 means queues of infinite size

#QueueWait
QueueWait = 0
#Here, 0 means non-blocking

#Command Messages

#View --> ViewController

ViewExit = "ViewExit"
NodeOn = "NodeOn"
NodeOff = "NodeOff"
EditBlackList = "EditBlackList"
NewMessageEditor = "NewMessageEditor"

NewBlackList = "NewBlackList"

def isNewBlackList(thing):
	try:
		if thing[0] == NewBlackList:
			return True
		else:
			return False
	except:
		return False


#PacketManager ->>

MyAddressIs = "MyAddressIs"
ResetRoutingTable = "ResetRoutingTable"

def isAddressMessage(thing):
	try:
		if thing[0] == MyAddressIs:
			return True
		else:
			return False
	except:
		return False

NewProcessedPacket = "NewProcessedPacket"

def isProcessedPacket(thing):
	try:
		if thing[0] == NewProcessedPacket:
			return True
		else:
			return False
	except:
		return False


#OGMProcessor ->>
OGMMessage = "OGMMessage"

def isOGMMessage(thing):
	try:
		if thing[0] == OGMMessage:
			return True
		else:
			return False
	except:
		return False

#Message Processor ->>
MessMessage = "MessMessage"

def isMessMessage(thing):
	try:
		if thing[0] == MessMessage:
			return True
		else:
			return False
	except:
		return False


#DataStorage ->>
UpdatedRoutingTable = "UpdatedRoutingTable"

def isUpdatedRoutingTable(thing):
	try:
		if thing[0] == UpdatedRoutingTable:
			return True
		else:
			return False
	except:
		return False

ReturnEditBlackList = "ReturnEditBlackList"

def isReturnEditBlackList(thing):
	try:
		if thing[0] == ReturnEditBlackList:
			return True
		else:
			return False
	except:
		return False

ConnectedNodes = "ConnectedNodes"

def isConnectedNodes(thing):
	try:
		if thing[0] == ConnectedNodes:
			return True
		else:
			return False
	except:
		return False

ReturnNewMessage = "ReturnNewMessage"

def isReturnNewMessage(thing):
	try:
		if thing[0] == ReturnNewMessage:
			return True
		else:
			return False
	except:
		return False



