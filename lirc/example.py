#!/usr/bin/env python

from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory
from LircReceiver import LircdProtocolFactory

def lircPrinter(code,pos,name,remote):
	print "%s @ %s    (%x,%i)"%(name,remote,code,pos)

lircd=LircdProtocolFactory(5,2)
lircd.addCallback(lircPrinter)

reactor.connectUNIX("/var/run/lirc/lircd", lircd)
reactor.run()