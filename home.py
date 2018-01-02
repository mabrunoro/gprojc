#!/usr/bin/env python3
import signal
from beacontools import BeaconScanner as bscanner, IBeaconFilter as bfilter
# import logging
import threading
import aws
# import os, sys
# import boto3

bdict = {}	# dictionary to store all beacons which will be listeed
UUID = None
scanner = None
TRIGGER = 60

# instead of using a beacon class, all attributes are stored in tuples
# class Beacon:
# 	def __init__(self,uuid,minor,major):
# 		self.uuid = uuid
# 		self.minor = minor
# 		self.major = major

def ehandler(signum, frame):
	# logging.warn("received signal " + str(signum))
	if(scanner is not None):
		# logging.warn("stopping scanner")
		scanner.stop()
	# logging.critical("bad exiting")
	# sys.exit(0)
	# os._exit(0)
	# threading.exit()

def handler(signum, frame):
	# logging.debug("1 second")
	for i in bdict.keys():
		bdict[i] = bdict[i] + 5
		if(((bdict[i] % TRIGGER) == 0) and (bdict[i] > 0)):	# waits one minute before setting beacon as lost
            # if this is not the first trigger, check this beacon status (it may have been found)
			if(bdict[i] > TRIGGER):
				item = aws.getitem(UUID, i[1], i[2])
				if(not item['Lost']):
					if('Date' in item):
						print("Beacon <%s,%d,%d> was found on %s" % (UUID, i[1], i[2], item['Date']))
						# logging.warn("beacon <%s,%d,%d> was found on %s" % (UUID, i[1], i[2], item['Date']))
					else:
						print("Beacon <%s,%d,%d> was found" % (str(UUID), i[1], i[2]))
						# logging.warn("beacon <%s,%d,%d> was found" % (str(UUID), i[1], i[2]))
					# bdict[i] = -1*TRIGGER	# reset beacon timer; if it doesn't arrive within two minutes, set it as lost again
				# else:
					# logging.warn("beacon <%s,%d,%d> lost" % (UUID, i[1], i[2]))
			else:
				# logging.warn("beacon <%s,%d,%d> lost" % (UUID, i[1], i[2]))
	            # set beacon as lost on AWS DynamoDB
				aws.setstatus(UUID, i[1], i[2], True)
	print(bdict)
	signal.signal(signal.SIGALRM, handler)
	signal.alarm(5)	# set alarm to the next second

# callback to check which beacon was found
def callback(bt_addr, rssi, packet, additional_info):
	# logging.debug("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))

    # if this beacon was lost, set it as found
	if(bdict[(packet.uuid, packet.minor, packet.major)] >= 60):
		print("Beacon <%s,%d,%d> was found" % (packet.uuid,packet.minor,packet.major))
		# logging.warn("beacon <%s,%d,%d> was found" % (packet.uuid,packet.minor,packet.major))
		aws.setstatus(packet.uuid, packet.minor, packet.major, False)

	bdict[(packet.uuid, packet.minor, packet.major)] = 0

# callback to show all devices available
def nofiltercb(bt_addr, rssi, packet, additional_info):
	pass
	# logging.debug(str(rssi) + ", " + str(packet.tx_power) + ", " + packet.uuid + ", " + str(packet.minor) + ", " + str(packet.major))

def scan():
	# logging.debug(UUID)

	global scanner

	if((UUID is None) or (UUID == "")):
		# logging.debug("creating scan without filter")
		scanner = bscanner(nofiltercb)
	else:
		# logging.debug("creating scan with filter uuid: " + UUID)
		scanner = bscanner(callback, device_filter=bfilter(uuid=UUID))
	# logging.info("scan start")
	# scanner._mon.daemon = True
	scanner.start()

def main(uuid=None, mm=[]):
	# logging.basicConfig(filename='home.log',level=logging.WARNING)
	if(uuid is None):
		pass
		# logging.info("no beacon uuid provided; listening all devices...")
	else:
		# logging.info("filtering beacons with uuid: " + uuid)
		global UUID	# otherwise a local UUID variable would be created
		UUID = uuid
		for i in mm:
			bdict[(uuid,i[0],i[1])] = 0

	signal.signal(signal.SIGALRM, handler)
	signal.signal(signal.SIGTERM, ehandler)
	signal.signal(signal.SIGINT, ehandler)
	signal.alarm(5)

	scan()

	# while(True):
	# 	pass
	# wait()

if(__name__ == "__main__"):
	main(uuid="b9407f30-f5f8-466e-aff9-25556b57fe6d",mm=[(4733, 37438), (4701, 28435), (1784, 25793)])

# ice: 1784/25793
# mint: 4701/28435
# blueberry: 4733/37438
