from random import randint
import time
import datetime
import requests
import json
import subprocess
import sys

class MyData():
	def __init__(self, index):
		self.clientId = str(self.getClientID(int(index)))
		self.lat = getCurrentLat()						
		self.long = getCurrentLong()
		self.edgemap = {"128.138.201.67", "10.0.0.237"}


	def getClientID(self, index):
		i = 0
		with open("clientIds.txt") as file:
			for id in file:
				if i == index:
					return id.strip()
				i +=1


def serverInteraction(map):
	response = ""
	i = 0
	try:
		while i < 5:
			if len(map) != 0:
				jsonData = json.dumps(map)
				print "JSON DATA: ",jsonData
				#edge-server: 52.38.209.208
				url = 'http://'+ map["ip"] + ":5000/pushSecondsData"
				response = requests.post(url, data=jsonData, headers={"Content-Type":"application/json"})
				#response = response

				print str(response)
				if "200" in str(response):
					break
				i += 1
				print
				print "Server didn't respond. Retrying..."
				time.sleep(1)
			else:
				break;
	except Exception as e:
		print "Error in sendData", str(e)


def sendData(time, data, clientId, ip):
	try:
		map = {}
		map["clientId"] = clientId
		map["data"] = data
		map["time"] = time
		map["ip"] = ip
		print
		serverInteraction(map)
			
	except Exception as e:
		print "Error in sendData: ", str(e)


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
	me = MyData(str(sys.argv[1]))
	ip = "10.0.0.237"	#getIp(me.edgemap)
	#print ip

	dataList = []
	fileIndex = str(randint(10,30))
	filename = "/home/vipra/ProjectReport2/dataset/" + fileIndex + "_dataset.txt";
	file = open(filename, 'r')
	
	for line in file:
		line = line.strip('\n')
		dataList.append(line)

	i = 0
	while True:
		now = datetime.datetime.now()
		try:
			sendData(str(now), dataList[i], me.clientId, ip)
		except Exception as e:
			print "Retrying..."

		#print "data sent", i
		i +=1
		
		if i > 95 :						#bcos we have just 96 lines in our dataset
			i =0
		'''
		datetm = datetime.datetime.strptime(str(now), "%Y-%m-%d %H:%M:%S.%f")
		
		if datetm.hour == 0 and datetm.minute == 0:
			if me.lat != getCurrentLat() and me.long != getCurrentLong():			# just to check if current location of client has changed
				me.lat = getCurrentLat()
				me.long = getCurrentLong()
				ip = getIp(me.edgemap)
		'''
		time.sleep(1)