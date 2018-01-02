#!/usr/bin/env python3
import boto3
# import logging

# logging.basicConfig(filename='aws.log',level=logging.WARNING)

def getitem(uuid, minor, major):
	table = boto3.resource('dynamodb').Table('Beacons')
	response = table.get_item(Key={'UUID/Minor/Major': uuid + '/' + str(minor) + '/' + str(major)})
	if('Item' in response):
		item = response['Item']
		# logging.info("returned item <%s,%d,%d> with lost status is %s" % (uuid,minor,major,item['Lost']))
	else:
		# logging.info("no item returned, which means it doesn't exist; item is now being created")
		item={'UUID/Minor/Major':uuid + '/' + str(minor) + '/' + str(major), 'Lost':True}
		table.put_item(Item=item)
	return item

def getstatus(uuid, minor, major):
	table = boto3.resource('dynamodb').Table('Beacons')
	response = table.get_item(Key={'UUID/Minor/Major': uuid + '/' + str(minor) + '/' + str(major)})
	if('Item' in response):
		item = response['Item']
		# logging.info("returned item <%s,%d,%d> with lost status is %s" % (uuid,minor,major,item['Lost']))
		return item['Lost']
	else:
		return False

def setstatus(uuid, minor, major, status=False, dt=None):
	table = boto3.resource('dynamodb').Table('Beacons')
    # automatically creates the item if it doesn't exist
	response = table.update_item(
									Key = { 'UUID/Minor/Major' :uuid + '/' + str(minor) + '/' + str(major) },
									UpdateExpression = 'SET Lost = :val1',
									ExpressionAttributeValues = { ':val1':status }
								)
	if(dt is not None):
		response = table.update_item(
										Key = { 'UUID/Minor/Major' :uuid + '/' + str(minor) + '/' + str(major) },
										UpdateExpression = 'SET Dtime = :val1',
										ExpressionAttributeValues = { ':val1':dt }
									)

# \033[X;Y;Z
# X is brightness, 0 for lighter, 1 for darker
# Y is text color
# Z is background color, 40 for black
class bcolors:
	black = '\033[0;30;40m'
	red = '\033[0;31;40m'
	green = '\033[0;32;40m'
	brown = '\033[0;33;40m'
	blue = '\033[0;34;40m'
	magenta = '\033[0;35;40m'
	cyan = '\033[0;36;40m'
	lgray = '\033[0;37;40m'
	dgray = '\033[1;30;40m'
	lred = '\033[1;31;40m'
	lgreen = '\033[1;32;40m'
	yellow = '\033[1;33;40m'
	lblue = '\033[1;34;40m'
	lmagenta = '\033[1;35;40m'
	lcyan = '\033[1;36;40m'
	white = '\033[1;37;40m'
	end = '\033[0m'

def main():
	t = bcolors.lcyan + 'AWS Functions Library' + bcolors.cyan + '''
	The objective of this library is to provide some functions to help communicate with Amazon Web Services.
	The service in use from Amazon is DynamoDB through boto3.
	The table is "Beacons", with fields UUID (String), Minor (Integer), Major (Integer) and Lost (Boolean).''' + bcolors.lcyan + '''
Functions''' + bcolors.lcyan + '''
	getstatus(uuid, minor, major)''' + bcolors.cyan + '''
		Returns the actual status on DynamoDB of the first beacon found with the provided information.''' + bcolors.lcyan + '''
	setstatus(uuid, minor, major, status)''' + bcolors.cyan + '''
		Sets the actual status on DynamoDB of the first beacon found with the provided information.
		If minor/major is -1, all beacons matching the rest of the info will be updated.
		status is optional, being "False" its default value, which means that the beacon(s) will be updated as found (not lost).''' + bcolors.end
	print(t)

if(__name__ == "__main__"):
	main()
