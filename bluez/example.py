#!/usr/bin/env python
# -*- coding: utf-8 -*-


from twisted.internet import reactor
from bluezSocket import bluezSocket
from twisted.protocols.basic import LineReceiver

def ramp(proto, val, add):
	#print val, "      ",
	proto.setChannel(0, val)
	if val>=255:
		add=-1
	if val<=0:
		add=1
	reactor.callLater(0.01*(255.0/float(val+1)), ramp, proto, val+add, add)

class testProto(LineReceiver):
	def setChannel(self, channel, value):
		self.sendLine("SEND %x:%x"%(channel,value))
		print ">> SEND %x:%x"%(channel,value)
	
	def lineReceived(self, line):
		print "<<",line
	
	def connectionMade(self):
		print "Connection made"
		
	def connectionLost(self,reason):
		print "Connection lost:",reason

if __name__ == "__main__":
	proto=testProto()
	bt=bluezSocket(proto, '00:18:E4:0C:68:0C', reactor)
	
	reactor.callLater(5, ramp, proto, 0, 1)
	reactor.callLater(120, reactor.stop)
	
	reactor.run()