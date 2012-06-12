from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import ReconnectingClientFactory

class LircdProtocol(LineReceiver):
	
	def __init__(self, ignoreInitial, repeatEvery):
		"""
		ignoreInitial: the amount of keypresses we ignore before the key should be repeated
		repeatEvery: key repeat rate after initial delay
		"""
		self.__ignoreInitial=int(ignoreInitial)
		self.__repeatEvery=int(repeatEvery)
		self.__callbacksFiltered=[]
		self.__callbacksUnfiltered=[]
		self.delimiter="\n"
	
	def lineReceived(self, line):
		try:
			(code,pos,name,remote)=line.split(" ")
			pos=int(pos, 16)
			code=int(code, 16)
		except:
			return
		
		for cb in self.__callbacksUnfiltered:
			cb(code,pos,name,remote)
		
		if pos==0 or (pos>=self.__ignoreInitial and ((pos-self.__ignoreInitial)%self.__repeatEvery)==0):
			for cb in self.__callbacksFiltered:
				cb(code,pos,name,remote)
	
	def addCallback(self, cbFun, getAll=False):
		if getAll:
			self.__callbacksUnfiltered.append(cbFun)
		else:
			self.__callbacksFiltered.append(cbFun)


class LircdProtocolFactory(ReconnectingClientFactory):
	def __init__(self, ignoreInitial, repeatEvery):
		self.proto=LircdProtocol(ignoreInitial, repeatEvery)
	
	def buildProtocol(self, addr):
		return self.proto
	
	def addCallback(self, cbFun, getAll=False):
		self.proto.addCallback(cbFun, getAll)