#!/usr/bin/env python3
# based on http://stackoverflow.com/a/20434019

import math

def calculateAccuracy(txPower, rssi):
	if(rssi == 0):
		return -1	# if we cannot determine accuracy, return -1

	ratio = float(rssi) / txPower
	if(ratio < 1.0):
		return math.pow(ratio, 10)
	else:
		return (0.89976) * math.pow(ratio, 7.7095) + 0.111
