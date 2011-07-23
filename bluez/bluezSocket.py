# -*- coding: utf-8 -*-
#
# Inserts a pybluez socket into the reactor main loop for asynchronous use inside twisted
#
# Based on http://twistedmatrix.com/trac/browser/tags/releases/twisted-11.0.0/twisted/internet/_posixserialport.py
# 
# 2011, GPL3


import bluetooth
from twisted.internet import abstract, fdesc

class bluezSocket(abstract.FileDescriptor):
	"""
	Beware: This class might throw bluetooth.BluetoothError Exceptions under several circumstances
	(e.g. when the other end is out of range).
	So you might want to catch these or they may crash your program.
	"""
	def __init__(self, protocol, device_id, reactor):
		"""
		protocol: A twisted IProtocol instance
		device_id: A Bluetooth "mac-address" as string (e.g. '00:11:22:33:44:55')
		reactor: a reactor
		"""
		self.connected = False
		self.device_id = device_id
		self.protocol = protocol
		self.reactor=reactor
		
		abstract.FileDescriptor.__init__(self, reactor)
		
		self.sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
		self.sock.connect((self.device_id,1))
		self.connected = True
		self.sock.setblocking(0)
		
		self.protocol.makeConnection(self)
		self.startReading()
	
	def fileno(self):
		return self.sock.fileno()
		
	def writeSomeData(self, data):
		return fdesc.writeToFD(self.fileno(), data)
	
	def doRead(self):
		return fdesc.readFromFD(self.fileno(), self.protocol.dataReceived)
	
	def connectionLost(self, reason):
		abstract.FileDescriptor.connectionLost(self, reason)
		self.sock.close()
		self.connected=False
		self.protocol.connectionLost(reason)