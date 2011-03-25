#! /usr/bin/env python
#***************************************
#	Filename: Plug.py
#	
#	Description:
#	This module is a wrapper class for two thread-safe
#	queues working together for two-way
#	communication between classes
#	
#***************************************

#Import Constants
from Constants import *

import Queue

class Plug:	
	def __init__(self, moduleNameOne, moduleNameTwo):
		self.queueDict = dict()	
		self.Queue_One = Queue.Queue(QueueSize)
		self.Queue_Two = Queue.Queue(QueueSize)	
		self.queueDict[moduleNameOne] = 1
		self.queueDict[moduleNameTwo] = 2

	def isEmpty(self, moduleName):

		if(self.queueDict[moduleName] == 1):	
				return self.Queue_Two.empty()	
			
		elif(self.queueDict[moduleName] == 2):
				return self.Queue_One.empty()	

	def get(self, moduleName):
		
		if(self.queueDict[moduleName] == 1):
			try:
				return self.Queue_Two.get(QueueWait)
			except Queue.Empty:
				return None
			
		elif(self.queueDict[moduleName] == 2):
			try:
				return self.Queue_One.get(QueueWait)
			except Queue.Empty:
				return None

	def put(self, thing, moduleName):
		
		if(self.queueDict[moduleName] == 1):
			self.Queue_One.put(thing, False)
			
		elif(self.queueDict[moduleName] == 2):
			self.Queue_Two.put(thing, False)

if __name__ == "__main__":

	plug = Plug()
	plug.connect("Jim", "Bob")
	
	plug.put("dude, you there bob", "Jim")
	plug.put("what's up jim", "Bob")

	print plug.get("Jim") + " when jim checked the mail"
	print plug.get("Bob") + " when bob checked the mail"
		
		
		
