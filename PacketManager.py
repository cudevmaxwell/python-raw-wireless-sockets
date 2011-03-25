#***************************************
#	Filename: PacketManager.py
#	
#	Description:
#	This module controls all of the low-level
#	packet sending/recieving.
#	
#***************************************

#Import Constants
from Constants import *

#My Imports:
import DefaultWhiteList

#Lib imports:
from threading import Thread
from subprocess import call
import time, random, sys, Queue, os, string, zlib, struct, fcntl, copy
from socket import *

class PacketManager(Thread):

	def __init__(self, ViewControllerPlug, DataStoragePlug, MessageProcessorPlug, OGMProcessorPlug):
		Thread.__init__(self)
		self.ViewControllerPlug = ViewControllerPlug
		self.DataStoragePlug = DataStoragePlug
		self.MessageProcessorPlug = MessageProcessorPlug
		self.OGMProcessorPlug = OGMProcessorPlug

	def run(self):

		if verbose: print "PacketManager Start"

		Exit = False		

		OGMSocket = None
		MessageSocket = None
		MyAddress = None
		NodeReady = False
		getAddress
		if useBlackList:
			blackList = list()
		else:
			tempAddress = getAddress()
			blackList = DefaultWhiteList.getWhiteList(tempAddress)
		

		while(not Exit):
			
			#check the view plug for messages
			if not self.ViewControllerPlug.isEmpty(__name__):
				viewControllerMessage = self.ViewControllerPlug.get(__name__)
				if viewControllerMessage != None:
					if viewControllerMessage == ViewExit:
						NodeReady = False
						Exit = True
						destroyInterface()
						if OGMSocket != None:
							OGMSocket.close()
						if MessageSocket != None:
							MessageSocket.close()
						if MyAddress != None:
							MyAddress == None
					elif viewControllerMessage == NodeOn:
						if NodeReady == False:
							MyAddress = setupInterface()
							OGMSocket = createOGMSocket()
							MessageSocket = createMessageSocket()
							NodeReady = True
							self.ViewControllerPlug.put(NodeOn, __name__)
							self.DataStoragePlug.put(NodeOn, __name__)
							self.MessageProcessorPlug.put(NodeOn, __name__)
							self.OGMProcessorPlug.put(NodeOn, __name__)
							txtAddress = mac2txt(MyAddress)
							self.DataStoragePlug.put((MyAddressIs, txtAddress), __name__)
							self.MessageProcessorPlug.put((MyAddressIs, txtAddress), __name__)
							self.OGMProcessorPlug.put((MyAddressIs, txtAddress), __name__)
							self.ViewControllerPlug.put((MyAddressIs, txtAddress), __name__)
							NodeReady = True
					elif viewControllerMessage == NodeOff:
						if NodeReady == True:
							NodeReady = False
							destroyInterface()
							if OGMSocket != None:
								OGMSocket.close()
							if MessageSocket != None:
								MessageSocket.close()
							if MyAddress != None:
								MyAddress == None
							self.ViewControllerPlug.put(NodeOff, __name__)
							self.DataStoragePlug.put(NodeOff, __name__)
							self.MessageProcessorPlug.put(NodeOff, __name__)
							self.OGMProcessorPlug.put(NodeOff, __name__)
					elif viewControllerMessage == EditBlackList:
						self.ViewControllerPlug.put((ReturnEditBlackList, copy.deepcopy(blackList)),  __name__)
					elif isNewBlackList(viewControllerMessage):
							blackList = copy.deepcopy(viewControllerMessage[1])
							self.DataStoragePlug.put(ResetRoutingTable, __name__)
						
							
		
			#check the data plug for messages					
					

			#check the message processor plug for messages
			if NodeReady:
				if not self.MessageProcessorPlug.isEmpty(__name__):
					messProcessorPlugMessage = self.MessageProcessorPlug.get(__name__)
					if messProcessorPlugMessage != None:
						if isMessMessage(messProcessorPlugMessage):
							self.ViewControllerPlug.put((NewProcessedPacket, "OUT", "MESS", \
														messProcessorPlugMessage[1], messProcessorPlugMessage[2],\
														messProcessorPlugMessage[3]),   __name__)	
							sendPacket(txt2mac(messProcessorPlugMessage[1]), txt2mac(messProcessorPlugMessage[2]),\
														 messProcessorPlugMessage[3], theMessageType, MessageSocket)

			#check the OGMProcessor plug for messages
			if NodeReady:
				if not self.OGMProcessorPlug.isEmpty(__name__):
					ogmProcessorPlugMessage = self.OGMProcessorPlug.get(__name__)
					if ogmProcessorPlugMessage != None:
						if isOGMMessage(ogmProcessorPlugMessage):
							self.ViewControllerPlug.put((NewProcessedPacket, "OUT", "OGM", \
														ogmProcessorPlugMessage[1], mac2txt(ogmProcessorPlugMessage[2]),\
														ogmProcessorPlugMessage[3]),   __name__)	
							sendPacket(txt2mac(ogmProcessorPlugMessage[1]), ogmProcessorPlugMessage[2],\
														 ogmProcessorPlugMessage[3], theOGMType, OGMSocket)



			#Check if there are any packets waiting in the socket buffers
			if NodeReady:
				#Recieve any OGM packets, and send them along to the OGM processor
				newestOGMPacket = recvPacket(OGMSocket)
				if newestOGMPacket != None:
					header = newestOGMPacket[0]
					payload = newestOGMPacket[1]
					sendAlongHeader = [None, None]
					sendAlongHeader[0] = mac2txt(header[1])
					sendAlongHeader[1] = mac2txt(header[0])	
					if useBlackList:	
						if sendAlongHeader[0].strip() not in blackList:
							self.ViewControllerPlug.put((NewProcessedPacket, "IN", "OGM", \
														sendAlongHeader[0], sendAlongHeader[1],\
														payload),   __name__)	
							self.OGMProcessorPlug.put((OGMMessage, sendAlongHeader, payload), __name__)
					else:	
						if sendAlongHeader[0].strip() in blackList:
							self.ViewControllerPlug.put((NewProcessedPacket, "IN", "OGM", \
														sendAlongHeader[0], sendAlongHeader[1],\
														payload),   __name__)	
							self.OGMProcessorPlug.put((OGMMessage, sendAlongHeader, payload), __name__)


				newestMessPacket = recvPacket(MessageSocket)
				if newestMessPacket != None:
					header = newestMessPacket[0]
					payload = newestMessPacket[1]
					sendAlongHeader = [None, None]
					sendAlongHeader[0] = mac2txt(header[1])
					sendAlongHeader[1] = mac2txt(header[0])		
					if useBlackList:
						if verbose: print MyAddress
						if verbose: print sendAlongHeader[1].strip()
						if sendAlongHeader[0].strip() not in blackList and \
										sendAlongHeader[1].strip() == mac2txt(MyAddress):
							self.ViewControllerPlug.put((NewProcessedPacket, "IN", "MESS", \
														sendAlongHeader[0], sendAlongHeader[1],\
														payload),   __name__)	
							self.MessageProcessorPlug.put((MessMessage, sendAlongHeader, payload), __name__)		
					else:
						if sendAlongHeader[0].strip() in blackList and \
										sendAlongHeader[1].strip() == mac2txt(MyAddress):
							self.ViewControllerPlug.put((NewProcessedPacket, "IN", "MESS", \
														sendAlongHeader[0], sendAlongHeader[1],\
														payload),   __name__)	
							self.MessageProcessorPlug.put((MessMessage, sendAlongHeader, payload), __name__)	
										
					
		
		if verbose: 
			print "PacketManager Exit"

def createOGMSocket():
	s = socket(AF_PACKET, SOCK_RAW, theOGMType)
	s.bind((theInterface,theOGMType))
	return s

def createMessageSocket():
	s = socket(AF_PACKET, SOCK_RAW, theMessageType)
	s.bind((theInterface,theMessageType))
	return s

def mac2txt(x):
	"""
	Based off code available: 
	http://www.secdev.org/projects/locator/files/locator.py
	Copyright (C) 2004  Philippe Biondi
	Converts a mac address into a human readable string.
	"""
	return "%02x:%02x:%02x:%02x:%02x:%02x" % tuple(map(ord,x))

def txt2mac(x):
	"""
	Converts a strings into a mac address
	"""
	returnMe = ''
	thelist = x.split(":")
	for item in thelist:
		returnMe = returnMe + item.decode("hex")
	return returnMe

def sendPacket(src, dest, data, protocol, sock):
	"""
	Send a packet.
	sendPacket(src, dest, data, protocol, sock)
	"""
	#This next line makes sure the header is network compatable (big endian) 
	sentFrame = struct.pack("!6s6sh",dest,src,protocol) + str(data)
	#Calculate CRC, make positive
	frameCRC = zlib.crc32(sentFrame) & 0xffffffff
	sentFrame = sentFrame + "/" + str(frameCRC)
	sock.send(sentFrame)	

def recvPacket(sock):
	"""
	Recv a packet.
	recvPacket(sock)
	Will only recv packets of size 2048
	Returns a tuple of the packet header and the packet data.
	"""
	sock.settimeout(socketTimeout)
	try:
		#Recieve the packet
		recvFrame = sock.recv(packetSizeRecv)
	
		#Get the header information
		recvPacketHeader = struct.unpack("!6s6sh",recvFrame[:14])
			
		#Process the packet for CRC
		recvPacketData = recvFrame[14:]
		recvPacketDataList = recvPacketData.split("/")
		recvPacketCRC = recvPacketDataList[len(recvPacketDataList)-1]
		newRecvFrame = str(recvFrame[:(len(recvFrame) - len(recvPacketCRC) - 1)])
		frameCRC = zlib.crc32(newRecvFrame) & 0xffffffff
		if str(recvPacketCRC).strip() != str(frameCRC).strip():
			print "recvPacketCRC: " + str(recvPacketCRC)
			print "frameCRC: " + str(frameCRC)
			return None	
		recvPacketData = newRecvFrame[14:]
		#Return the recieved packet that passed the CRC test
		return (recvPacketHeader, recvPacketData)
	except:
		return None

def setupInterface():
	"""
	Run the setup routine on the given interface.
	Returns the mac address of the interface.
	"""
	if verbose: sys.stdout.write("Preparing wireless interface...")
	call(["iwconfig", theInterface, "mode", "ad-hoc"])
	call(["iwconfig", theInterface, "essid", essid])
	call(["iwconfig", theInterface, "channel", channel])
	call(["iwconfig", theInterface, "rate", "auto"])
	call(["ifconfig", theInterface, "up"])

	if verbose: sys.stdout.write("Done!\n\n")
	if verbose: call(["iwconfig", theInterface]) 
	
	s = socket(PF_PACKET, SOCK_RAW)
	s.bind((theInterface, 0))
	returnMe = s.getsockname()[4]
	if verbose: sys.stdout.write("My Address:" + mac2txt(returnMe) + "\n")
	s.close()
	return returnMe

def getAddress():
	s = socket(PF_PACKET, SOCK_RAW)
	s.bind((theInterface, 0))
	returnMe = s.getsockname()[4]
	if verbose: sys.stdout.write("My Address:" + mac2txt(returnMe) + "\n")
	s.close()
	return mac2txt(returnMe)

def destroyInterface():
	"""
	Bring down the given interface.
	"""
	if verbose: sys.stdout.write("Bringing down wireless interface...")
	call(["ifconfig", theInterface, "down"])
	if verbose: sys.stdout.write("Done!\n\n")
	if verbose:	call(["ifconfig", theInterface]) 



		


