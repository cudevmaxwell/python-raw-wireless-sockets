#***************************************
#	FileName: DefaultWhiteList.py
#
#	Description:
#	This file contains a default whitelist
#	used when the program is first started. 
#
#****************************************

ipToMacAddress = {182:"00:02:2d:41:45:f2", \
183:"00:02:2d:49:94:b7", \
174:"00:02:2d:3a:48:dd", \
203:"00:02:2d:3b:e9:2b", \
184:"00:60:1d:f0:9c:9d", \
193:"00:60:1d:1e:91:a4", \
196:"00:60:1d:1d:18:3a", \
197:"00:60:1d:f0:9c:77"}

def getWhiteList(address):

	#For computer with ip=192.168.0.203:
	if address == ipToMacAddress[203]:
		#This machine can see 174 and 183:
		return [ ipToMacAddress[174],  ipToMacAddress[183]]
	#For computer with ip=192.168.0.174:
	elif address == ipToMacAddress[174]:
		#This machine can see 203:
		return [ ipToMacAddress[203]]
	#For computer with ip=192.168.0.183:
	elif address == ipToMacAddress[183]:
		#This machine can see 203 and 183:
		return [ ipToMacAddress[203], ipToMacAddress[182]]
	#For computer with ip=192.168.0.182:
	elif address == ipToMacAddress[182]:
		#This machine can see 183:
		return [ ipToMacAddress[183]]
	else: 
		return list()


