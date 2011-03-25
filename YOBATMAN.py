#! /usr/bin/env python
#***************************************
#	Filename: YOBATMAN.py
#	
#	Description:
#	This is the bootstrap script, used to get
#	the rest of the threads running. 
#	
#***************************************

#Import Constants
from Constants import *

#Import the other modules
import ViewController, DataStorage, PacketManager, OGMProcessor, MessageProcessor, Plug

#First, create the nine plugs we'll need to connect the various threads
ViewController_PacketManager = Plug.Plug("ViewController", "PacketManager")
ViewController_OGMProcessor = Plug.Plug("ViewController", "OGMProcessor")
ViewController_MessageProcessor = Plug.Plug("ViewController", "MessageProcessor")
ViewController_DataStorage = Plug.Plug("ViewController", "DataStorage")
DataStorage_PacketManager = Plug.Plug("DataStorage", "PacketManager")
DataStorage_OGMProcessor = Plug.Plug("DataStorage", "OGMProcessor")
DataStorage_MessageProcessor = Plug.Plug("DataStorage", "MessageProcessor")
PacketManager_OGMProcessor = Plug.Plug("PacketManager", "OGMProcessor")
PacketManager_MessageProcessor = Plug.Plug("PacketManager", "MessageProcessor")

#Next, create the five classes, and connect the plugs together

myViewController = ViewController.ViewController(ViewController_DataStorage, ViewController_PacketManager, ViewController_MessageProcessor, ViewController_OGMProcessor)

myDataStorage = DataStorage.DataStorage(ViewController_DataStorage, DataStorage_PacketManager, DataStorage_OGMProcessor, DataStorage_MessageProcessor)

myPacketManager = PacketManager.PacketManager(ViewController_PacketManager, DataStorage_PacketManager, PacketManager_MessageProcessor, PacketManager_OGMProcessor)

myOGMProcessor = OGMProcessor.OGMProcessor(ViewController_OGMProcessor, DataStorage_OGMProcessor, PacketManager_OGMProcessor)

myMessageProcessor = MessageProcessor.MessageProcessor(ViewController_MessageProcessor, DataStorage_MessageProcessor, PacketManager_MessageProcessor)

#Start up the threads

#print if acting as blacklist or whitelist

print "Blacklist: " + str(useBlackList)

myViewController.start()
myDataStorage.start()
myPacketManager.start()
myOGMProcessor.start()
myMessageProcessor.start()

#Wait for the threads to exit
myViewController.join()
myDataStorage.join()
myPacketManager.join()
myOGMProcessor.join()
myMessageProcessor.join()

#Say goodbye
print "Goodbye!"







