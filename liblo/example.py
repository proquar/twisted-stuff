#!/usr/bin/env python
# -*- coding: utf-8 -*-


from twisted.internet import reactor
from libloSocket import LibloSocket

def libloPrinter(path, args, types, src, user_data):
	print "Path:",path
	print "Arguments:",args
	print "Types:",types
	print "Source:",src
	print "User data:",user_data
	print "-----------------------------------"


if __name__ == "__main__":
	osc=LibloSocket(reactor, 6789)
	
	osc.addMethod("/test", None, libloPrinter, ("some","user","data"))
	
	reactor.callLater(120, reactor.stop)
	print osc.getURL()
	
	reactor.run()