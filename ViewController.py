#***************************************
#	Filename: ViewController.py
#	
#	Description:
#	This module is the controller for the GUI.
#	All of the other modules route messages
#	to and from the GUI through this module.
#	
#***************************************

#Import Constants
from Constants import *

#Lib imports:
from threading import Thread
import wx, Queue

#My Module Imports
import View

class ViewController(Thread):

	def __init__(self, DataStoragePlug, PacketManagerPlug, MessageProcessorPlug, OGMProcessorPlug):
		Thread.__init__(self)
		self.DataStoragePlug = DataStoragePlug
		self.PacketManagerPlug = PacketManagerPlug
		self.MessageProcessorPlug = MessageProcessorPlug
		self.OGMProcessorPlug = OGMProcessorPlug
		self.guiApp = View.YOBATMANGUI(0)
		self.GUIStarter = GUIStarter(self.guiApp)
		self.ViewEventQueue = Queue.Queue(QueueSize)
		self.BlackListEditQueue = Queue.Queue(1)
		self.NewMessageQueue = Queue.Queue(1)

	def exit(self, event):
		self.ViewEventQueue.put(ViewExit)
	
	def nodeOn(self, event):
		self.ViewEventQueue.put(NodeOn)

	def nodeOff(self, event):
		self.ViewEventQueue.put(NodeOff)
	
	def editBlackList(self, event):
		self.ViewEventQueue.put(EditBlackList)

	def newMessage(self, event):
		if verbose: print "newmess button"
		self.ViewEventQueue.put(NewMessageEditor)

	def run(self):	

		if verbose: print "ViewController Start"

		#Add bindings for GUI elements		
		self.guiApp.mainFrame.Bind(wx.EVT_MENU, self.exit, id=9)
		self.guiApp.mainFrame.Bind(wx.EVT_MENU, self.nodeOn, id=1)
		self.guiApp.mainFrame.Bind(wx.EVT_MENU, self.nodeOff, id=2)
		self.guiApp.mainFrame.Bind(wx.EVT_MENU, self.editBlackList, id=3)
		self.guiApp.mainFrame.Bind(wx.EVT_BUTTON, self.newMessage, id=10)
		self.guiApp.mainFrame.Bind(wx.EVT_CLOSE, self.exit)

		#Start the GUI
		self.GUIStarter.start()

		Exit = False
		
		while(not Exit):
			
			#check the data plug for messages
			if not self.DataStoragePlug.isEmpty(__name__):
				dataStorageMessage = self.DataStoragePlug.get(__name__)
				if dataStorageMessage != None:
					if isUpdatedRoutingTable(dataStorageMessage):
						wx.CallAfter(self.guiApp.mainFrame.UpdateList, dataStorageMessage[1], dataStorageMessage[2])
					elif isConnectedNodes(dataStorageMessage):
						connectedNodeList = dataStorageMessage[1]
						wx.CallAfter(self.guiApp.mainFrame.StartUpMessageEditor, connectedNodeList, self.NewMessageQueue)
												
					
			#check the packetmanager plug for messages
			if not self.PacketManagerPlug.isEmpty(__name__):
				packetManagerMessage = self.PacketManagerPlug.get(__name__)
				if packetManagerMessage != None:
					if packetManagerMessage == NodeOn:
						wx.CallAfter(self.guiApp.mainFrame.NodeStatusUpdate, True)
					elif packetManagerMessage == NodeOff:
						wx.CallAfter(self.guiApp.mainFrame.NodeStatusUpdate, False)	
					elif isProcessedPacket(packetManagerMessage):
						wx.CallAfter(self.guiApp.mainFrame.UpdateList, 0, packetManagerMessage[1:])		
					elif isReturnEditBlackList(packetManagerMessage):
						blacklist = packetManagerMessage[1]
						wx.CallAfter(self.guiApp.mainFrame.StartUpBlackListEditor, blacklist, self.BlackListEditQueue)
					elif isAddressMessage(packetManagerMessage):
						myAddress = packetManagerMessage[1]
						wx.CallAfter(self.guiApp.mainFrame.UpdateTitle, myAddress)							
				

			#check the message processor plug for messages
			if not self.MessageProcessorPlug.isEmpty(__name__):
					messProcessorPlugMessage = self.MessageProcessorPlug.get(__name__)
					if messProcessorPlugMessage != None:
						if isReturnNewMessage(messProcessorPlugMessage):
							wx.CallAfter(self.guiApp.mainFrame.UpdateList, 3, messProcessorPlugMessage[1])
			#check the ogm processor plug for messages		

			#Check the ViewEvent Queue
			if self.ViewEventQueue.qsize() != 0:
				viewCommand = self.ViewEventQueue.get(QueueWait)
				if viewCommand == ViewExit:
					Exit = True
					self.DataStoragePlug.put(ViewExit, __name__)
					self.PacketManagerPlug.put(ViewExit, __name__)
					self.MessageProcessorPlug.put(ViewExit, __name__)
					self.OGMProcessorPlug.put(ViewExit, __name__)	
					self.guiApp.mainFrame.Destroy()
					self.GUIStarter.join()	
									
				elif viewCommand == NodeOn:
					self.PacketManagerPlug.put(NodeOn, __name__)
				elif viewCommand == NodeOff:
					self.PacketManagerPlug.put(NodeOff, __name__)
				elif viewCommand == EditBlackList:
					self.PacketManagerPlug.put(EditBlackList, __name__)
				elif viewCommand == NewMessageEditor:
					self.DataStoragePlug.put(NewMessageEditor, __name__)

			#Check the edit blacklist queue
			if not self.BlackListEditQueue.empty():
				newBlackList = self.BlackListEditQueue.get(QueueWait)
				self.PacketManagerPlug.put((NewBlackList, newBlackList), __name__)

			#Check the new message queue
			if not self.NewMessageQueue.empty():
				newMessage = self.NewMessageQueue.get(QueueWait)
				self.MessageProcessorPlug.put((ReturnNewMessage, newMessage), __name__)		
					
					

		if verbose: print "ViewController Exit"

class GUIStarter(Thread):

	def __init__(self, GuiApp):
		Thread.__init__(self)
		self.GuiApp = GuiApp

	def run(self):
		self.GuiApp.MainLoop()	

	
		
