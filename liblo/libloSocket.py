# -*- coding: utf-8 -*-
#
# Inserts a liblo socket into the reactor main-loop
#
# Based on this: https://github.com/jdavisp3/twisted-intro/blob/master/twisted-client-1/get-poetry.py
#
# 2011, GPL3
#

import liblo

class LibloSocket(object):
	
	def __init__(self, reactor, port=None, proto=liblo.UDP):
		self.portnum=port
		self.reactor=reactor
		self.proto=proto
		
		self.reactor.addReader(self)
		self.server=liblo.Server(self.portnum, self.proto)
		self.connected=True
	
	def addMethod(self, path, typespec, callback_func, user_data=None):
		#if user_data:
			self.server.add_method(path, typespec, callback_func, user_data)
		#else:
			#self.server.add_method(path, typespec, callback_func)
	
	def send(self, target, content):
		self.server.send(target, content)
	
	def getURL(self):
		return self.server.get_url()
	
	def getPort(self):
		return self.server.get_port()
	
	
	def fileno(self):
		return self.server.fileno()
	
	def doRead(self):
		while self.server.recv(0):
			pass
		return None
	
	def logPrefix(self):
		return "Liblo: "+str(self.getURL())
	
	def connectionLost(self, reason):
		self.server.free()
		self.reactor.removeReader(self)
		self.connected=False