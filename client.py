from random import randint
import time
import datetime
import socket
import requests
import json
import subprocess

class MyData():
	def __init__(self):
		self.clientId = str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9))
		self.lat = getCurrentLat()						
		self.long = getCurrentLong()
		self.edgemap = {"8.8.8.8", "www.facebook.com", "www.youtube.com"}


def serverInteraction(map):
	response = ""

	if len(map) != 0:
		while (True):
			'''sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			sock.setblocking(False)

			send = sock.sendto(data,(address, int(port)))
			time.sleep(2)
			try :
				response, server  = sock.recvfrom(10240)
				print "Response: ", response
				if (response != None):
					break
				if response == "":
					raise Exception
			except:
				print "Server didn't respond."
				tries +=1
				if (tries < 6):
					print "Trying Again ", tries, "..."
				else:
					print "Server is responding."
					break
	return response
	'''


def sendData(time, data, clientId):
	try:
		map = {}
		map["clientId"] = clientId
		map["data"] = data
		map["time"] = time
		print
		print "Request's Data:", task
		serverInteraction(map)
			
	except socket.error, msg:
		print ("Error during sending message.")
		print ("ERROR CODE: ", msg[0])
		print ("ERROR MESSAGE: ", msg[1])


def getCurrentLat():			# got from GPS
	return "40.0292888"


def getCurrentLong():			# got from GPS
	return "-105.3100174"


def getIp(ipMap):
	minHops = 9999
	minIp = ""
	
	for ip in ipMap:
	    command = "traceroute " + ip
	    
	    print "IP: ", ip
	    traceroute = subprocess.Popen(["traceroute", '-w', '100',ip],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	    for line in iter(traceroute.stdout.readline,""):
	        str = line

	    print str
	    index = str.index(' ')
	    str = str[0:index]
	    
	    if minHops > int(str):
	    	minHops = int(str)
	    	minIp = ip
	
	return minIp



if __name__ == '__main__':
	i = 0
	me = MyData()
	ip = getIp(me.edgemap)
	print ip

	dataList = []
	fileIndex = str(randint(10,30))
	filename = "/dataset/" + fileIndex + "_dataset.txt";

	file = open(filename, 'r')
	
	for line in file:
		line = line.strip('\n')
		dataList.append(line)

	i = 0
	while true:
		now = datetime.datetime.now()
		sendData(str(now), dataList[i], me.clientId)
		i +=1
		
		if i > 95 :						#bcos we have just 96 lines in our dataset
			i =0
		
		datetm = datetime.datetime.strptime(str(now), "%Y-%m-%d %H:%M:%S.%f")
		if datetm.hour == 0 && datetm.minute == 0
			if me.lat != getCurrentLat() && me.long != getCurrentLong()			# just to check if current location of client has changed
				me.lat = getCurrentLat()
				me.long = getCurrentLong()
				ip = getIp(me.edgemap)

		time.sleep(3000)