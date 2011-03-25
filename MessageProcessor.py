#***************************************
#	Filename: MessageProcessor.py
#	
#	Description:
#	This module processes all of the sent and
#	recieved Message packets.
#	
#***************************************

#Import Constants
from Constants import *

#Lib imports:
from threading import Thread
import string

class MessageProcessor(Thread):

	def __init__(self, ViewControllerPlug, DataStoragePlug, PacketManagerPlug):
		Thread.__init__(self)
		self.ViewControllerPlug = ViewControllerPlug
		self.DataStoragePlug = DataStoragePlug
		self.PacketManagerPlug = PacketManagerPlug

	def run(self):

		if verbose: print "MessageProcessor Start"
		myAddress = None
		theNodeisOn = False
		Exit = False
		
		while(not Exit):
			
			#check the view plug for messages
			if not self.ViewControllerPlug.isEmpty(__name__):
				viewControllerMessage = self.ViewControllerPlug.get(__name__)
				if viewControllerMessage != None:
					if viewControllerMessage == ViewExit:
						Exit = True
					elif isReturnNewMessage(viewControllerMessage):
						recievedMessage = viewControllerMessage[1]			
						if verbose: print "MessPross got message: " + str(recievedMessage)			
						if recievedMessage[0] != '' and recievedMessage[1] != '' and theNodeisOn and myAddress != None:
							#Here, we build the message to send. 
							if verbose: print "MessPross building mess"		
							payload = str(ttl_value) + "/" + str(recievedMessage[0]) + "/" + myAddress + "/" + str(recievedMessage[1])
							finalDest =  str(recievedMessage[0])
							#Ask the dataStorage who we should send this message to:
							self.DataStoragePlug.put((MessMessage, finalDest, payload), __name__)
	
	
			#check the data plug for messages
			if not self.DataStoragePlug.isEmpty(__name__):
				dataStorageMessage = self.DataStoragePlug.get(__name__)
				if dataStorageMessage != None:
					if isMessMessage(dataStorageMessage):
						bestNext = dataStorageMessage[1]
						payload = dataStorageMessage[2]
						if verbose: print "HEY GOT THE MESS BACK FROM DATA: " + str(bestNext)
						self.PacketManagerPlug.put((MessMessage, myAddress, bestNext, payload), __name__)					

			#check the packetmanager plug for messages
			if not self.PacketManagerPlug.isEmpty(__name__):
				packetManagerMessage = self.PacketManagerPlug.get(__name__)
				if packetManagerMessage != None:
					if packetManagerMessage == NodeOn:
						theNodeisOn = True
					elif packetManagerMessage == NodeOff:
						theNodeisOn = False
					elif isAddressMessage(packetManagerMessage):
						myAddress = packetManagerMessage[1]
					elif isMessMessage(packetManagerMessage):
						print "Recieved message! MESSAGE PROCESSOR : " + str(packetManagerMessage[1:])
						recievedMessagePayload = packetManagerMessage[2]
						listFromPayload = recievedMessagePayload.split("/")
						ttl_fromPayload = listFromPayload[0]
						theFinalDest = listFromPayload[1]
						theOriginator = listFromPayload[2]
						theMessage =  listFromPayload[3]
						if theFinalDest == myAddress:
							self.ViewControllerPlug.put((ReturnNewMessage, (theOriginator, theMessage)),   __name__)
						else:
							if ttl_fromPayload > 0:
								listFromPayload[0] = str(int(ttl_fromPayload)-1)
								newMessage = string.join(listFromPayload, "/")
								self.DataStoragePlug.put((MessMessage, theFinalDest, newMessage), __name__)

		if verbose: print "MessageProcessor Exit"
