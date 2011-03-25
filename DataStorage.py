#***************************************
#	Filename: MessageProcessor.py
#	
#	Description:
#	This module stores and returns the collected
#	data for the program.
#	
#***************************************

#Import Constants
from Constants import *

#Lib imports:
from threading import Thread
import copy, time

class DataStorage(Thread):

	def __init__(self, ViewControllerPlug, PacketManagerPlug, OGMProcessorPlug, MessageProcessorPlug):
		Thread.__init__(self)
		self.ViewControllerPlug = ViewControllerPlug
		self.PacketManagerPlug = PacketManagerPlug
		self.OGMProcessorPlug = OGMProcessorPlug
		self.MessageProcessorPlug = MessageProcessorPlug

	def run(self):

		if verbose: print "DataStorage Start"
		routingDict = dict()
		myAddress = None
		theNodeisOn = False
		wallTime = time.clock()	
		Exit = False
		
		while(not Exit):	

				
			
			#check the view plug for messages
			if not self.ViewControllerPlug.isEmpty(__name__):
				viewControllerMessage = self.ViewControllerPlug.get(__name__)
				if viewControllerMessage != None:
					if viewControllerMessage == ViewExit:
						Exit = True
					if viewControllerMessage == NewMessageEditor:
						self.ViewControllerPlug.put((ConnectedNodes, routingDict.keys() ), __name__)
						
	
			#check the PacketManager plug for messages
			if not self.PacketManagerPlug.isEmpty(__name__):
				packetManagerMessage = self.PacketManagerPlug.get(__name__)
				if packetManagerMessage != None:
					if packetManagerMessage == NodeOn:
						theNodeisOn = True
					elif packetManagerMessage == NodeOff:
						theNodeisOn = False
					elif isAddressMessage(packetManagerMessage):
						myAddress = packetManagerMessage[1]
					elif packetManagerMessage == ResetRoutingTable:
						routingDict = dict()
						self.ViewControllerPlug.put((UpdatedRoutingTable, 1, copy.deepcopy(routingDict)), __name__)

			#check the OGMProcessor plug for messages
			if not self.OGMProcessorPlug.isEmpty(__name__):
				ogmProcessorMessage = self.OGMProcessorPlug.get(__name__)
				if ogmProcessorMessage != None:
					if isOGMMessage(ogmProcessorMessage):
						#Process packet to see if routing table will need to be updated
						changes = False
						header = ogmProcessorMessage[1]
						payload = ogmProcessorMessage[2]
						sender = header[0]					
						listFromPayload = payload.split("/")
						timeToLive = listFromPayload[0]
						originator = listFromPayload[1]
						sequenceNumber = listFromPayload[2]
						timeBeforeRemoval = (timeBetweenOGM + maxRandomTimeBetweenOGM) * 2
						
						if originator not in routingDict and originator != myAddress:
							routingDict[originator] = (sender, timeToLive, sequenceNumber, timeBeforeRemoval)
							changes = True
						elif originator in routingDict and routingDict[originator][2] < sequenceNumber and routingDict[originator][1] < timeToLive:
							routingDict[originator] = (sender, timeToLive, sequenceNumber, timeBeforeRemoval)
							changes = True
						elif originator in routingDict and routingDict[originator][2] < sequenceNumber:
							oldSender = routingDict[originator][0]
							oldTTL = routingDict[originator][1]
							routingDict[originator] = (oldSender, oldTTL, sequenceNumber, timeBeforeRemoval)
						if changes:
							self.ViewControllerPlug.put((UpdatedRoutingTable, 1, copy.deepcopy(routingDict)),   __name__)			
						

			#check the MessageProcessor for messages
			if not self.MessageProcessorPlug.isEmpty(__name__):
				messProcessorMessage = self.MessageProcessorPlug.get(__name__)
				if messProcessorMessage != None:					
					if isMessMessage(messProcessorMessage):
						finalDest = messProcessorMessage[1]
						payload = messProcessorMessage[2]
						bestDest =  str(routingDict[finalDest][0])
						if verbose: print "DataStorage best dest for message:"  + str(bestDest)
						self.MessageProcessorPlug.put((MessMessage, bestDest, payload), __name__)

			#has 1 second gone by?
			currentTime = time.clock()
			if currentTime - wallTime >= 1 and theNodeisOn:
				wallTime = time.clock()
				deleteLaterList = []
				for k,v in routingDict.iteritems():
					oldEntry = routingDict[k]
					newTimeTillRemoval = oldEntry[3] - 1
					if newTimeTillRemoval <= 0:
						deleteLaterList.append(k)
					else:
						routingDict[k] = (oldEntry[0], oldEntry[1], oldEntry[2], newTimeTillRemoval)
				for item in deleteLaterList:
					del routingDict[item]
				self.ViewControllerPlug.put((UpdatedRoutingTable, 1, copy.deepcopy(routingDict)),   __name__)			
				
		

		if verbose: print "DataStorage Exit"
