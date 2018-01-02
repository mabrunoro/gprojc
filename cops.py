#!/usr/bin/env python3

import signal
from beacontools import BeaconScanner as bscanner, IBeaconFilter as bfilter
# import logging
import datetime
import aws
# import boto3
# import sys

bdict = {}	# dictionary to store all beacons whose status will be checked
scanner = None
TRIGGER = 30

# instead of using a beacon class, all attributes are stored in tuples
# class Beacon:
# 	def __init__(self,uuid,minor,major):
# 		self.uuid = uuid
# 		self.minor = minor
# 		self.major = major

def handler(signum, frame):
	# logging.debug("1 second")
	toremove = []
	for i in bdict.keys():
		# wait 30 seconds before checking if beacon is lost
        # if it's not lost after 1 minute, remove it from the dictionary
        # whenever the server says it's lost, tell it you've found it <value on bdict> seconds ago
		if((bdict[i] % TRIGGER) == 0):
			# logging.info("checking if beacon <%s,%d,%d> is lost" % (i[0], i[1], i[2]))
            # gets beacon status from AWS DynamoDB
			lost = aws.getstatus(i[0], i[1], i[2])
			if(lost):
				print("Beacon <%s,%d,%d> found" % (i[0], i[1], i[2]))
				# logging.warn("beacon <%s,%d,%d> found" % (i[0], i[1], i[2]))
				now = (datetime.datetime.now() - datetime.timedelta(seconds=bdict[i])).strftime("%H:%M:%S %d/%m/%y")
                # set beacon as found on AWS DynamoDB, and possibly send your location
				aws.setstatus(i[0], i[1], i[2], False, dt=now)
				toremove.append((i[0], i[1], i[2]))
			elif(bdict[i] == 2*TRIGGER):
                # if beacon is still not lost after 1 minute, remove it from your dictionary
				toremove.append((i[0], i[1], i[2]))
		bdict[i] = bdict[i] + 5
	for i in toremove:
		bdict.pop(i, None)
	print(bdict)
	# bdict[i] = bdict[i] + 1
	signal.signal(signal.SIGALRM, handler)
	signal.alarm(5)	# set alarm to the next second

# handler for other signals
def ehandler(signum, frame):
	# logging.warn("received signal " + str(signum))
	if(scanner is not None):
		# logging.warn("stopping scanner")
		scanner.stop()

# callback to show all devices available
def nofiltercb(bt_addr, rssi, packet, additional_info):
	# logging.debug("%d, %s, %d, %d" % (rssi, packet.uuid, packet.minor, packet.major))
	if((packet.uuid, packet.minor, packet.major) not in bdict):
		bdict[(packet.uuid, packet.minor, packet.major)] = 0

def scan():
	global scanner	# otherwise a local scanner variable would be created
	# logging.debug("creating scan without filter")
	scanner = bscanner(nofiltercb)
	# logging.info("scan start")
	scanner.start()

def main(uuid=None, mm=[]):
	# logging.basicConfig(filename='cops.log',level=logging.WARNING)
	# logging.info("listening all devices...")

	signal.signal(signal.SIGTERM, ehandler)
	signal.signal(signal.SIGINT, ehandler)
	signal.signal(signal.SIGALRM, handler)
	signal.alarm(5)

	scan()

	# while(True):
	# 	pass
	# wait()

if(__name__ == "__main__"):
	main()
