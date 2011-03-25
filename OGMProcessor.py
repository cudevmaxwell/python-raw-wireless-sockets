#***************************************
#	Filename: OGMProcessor.py
#	
#	Description:
#	This module processes all of the sent and
#	recieved OGM packets.
#	
#***************************************

#Import Constants
from Constants import *

#Lib imports:
from threading import Thread
import time, random, string

class OGMProcessor(Thread):

	def __init__(self, ViewControllerPlug, DataStoragePlug, PacketManagerPlug):
		Thread.__init__(self)
		self.ViewControllerPlug = ViewControllerPlug
		self.DataStoragePlug = DataStoragePlug
		self.PacketManagerPlug = PacketManagerPlug

	def run(self):

		if verbose: print "OGMProcessor Start"

		Exit = False
		theNodeisOn = False
		myAddress = None
		wallTime = time.clock()
		sequenceNumber = sequenceNumberStart
		alreadyRepeated = dict()
		
		while(not Exit):
			
			#check the view plug for messages
			if not self.ViewControllerPlug.isEmpty(__name__):
				viewControllerMessage = self.ViewControllerPlug.get(__name__)
				if viewControllerMessage != None:
					if viewControllerMessage == ViewExit:
						Exit = True
						
	
			#check the data plug for messages

			#check the packetmanager plug for messages
			if not self.PacketManagerPlug.isEmpty(__name__):
				packetManagerMessage = self.PacketManagerPlug.get(__name__)
				if packetManagerMessage != None:
					if packetManagerMessage == NodeOn:
						theNodeisOn = True
						if verbose: print "OGMProcessor: NodeOn"
					elif packetManagerMessage == NodeOff:
						theNodeisOn = False
						if verbose: print "OGMProcessor: NodeOff"
					elif isAddressMessage(packetManagerMessage):
						myAddress = packetManagerMessage[1]
						if verbose: print "OGMProcessor: MY address is: " + myAddress
					elif isOGMMessage(packetManagerMessage):
						header = packetManagerMessage[1]
						payload = packetManagerMessage[2]
						sender = header[0]
						self.DataStoragePlug.put((OGMMessage, header, payload), __name__)
						listFromPayload = payload.split("/")
						ttl_ofpacket = listFromPayload[0]
						originator = listFromPayload[1]
						sequenceNumberOfPacket = listFromPayload[2]	
						if originator != myAddress:								
							if ttl_ofpacket > 0:							
								if alreadyRepeated.has_key(originator):	
									if verbose: print str(alreadyRepeated)		
									if verbose: print "alreadyRepeated[originator]: " + str(alreadyRepeated[originator])
									if verbose: print " sequenceNumberOfPacket: " + str(sequenceNumberOfPacket)
									if alreadyRepeated[originator] < sequenceNumberOfPacket:		
										alreadyRepeated[originator] = sequenceNumberOfPacket							
										listFromPayload[0] = str(int(listFromPayload[0]) -1)
										returnedPayload = string.join(listFromPayload, "/")		
										self.PacketManagerPlug.put((OGMMessage, myAddress, BROADCAST, returnedPayload), __name__)				
										if verbose: print "packetManagerPlug.put:" + returnedPayload
								else:
									alreadyRepeated[originator] = sequenceNumberOfPacket						
									listFromPayload[0] = str(int(listFromPayload[0]) -1)						
									returnedPayload = string.join(listFromPayload, "/")
									self.PacketManagerPlug.put((OGMMessage, myAddress, BROADCAST, returnedPayload), __name__)
								
									
				
	
						
				
			#Alright, now we do some work:
			if theNodeisOn and (myAddress != None):
				#Check the current time:
				currentTime = time.clock()
				#Is the old time + timeBetweenOGM > currentTime? 
				if (currentTime - wallTime) > timeBetweenOGM:					
					#Sleep for an extra random amount of time					
					time.sleep(random.random() * maxRandomTimeBetweenOGM)
					wallTime = time.clock()
					data = str(ttl_value) + "/" + myAddress + "/" + str(sequenceNumber)
					self.PacketManagerPlug.put((OGMMessage, myAddress, BROADCAST, data), __name__)
					sequenceNumber = sequenceNumber + 1 

		if verbose: print "OGMProcessor Exit"
