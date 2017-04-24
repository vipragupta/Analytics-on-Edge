from random import randint
import time
import datetime
import socket
import requests
import json
import subprocess

class MyData():
	def __init__(self):
		self.clientId = str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9))+ str(randint(0,9))+ str(randint(0,9)) + str(randint(0,9))+ str(randint(0,9))+ str(randint(0,9))
		self.lat = getCurrentLat()						
		self.long = getCurrentLong()
		self.edgemap = {"8.8.8.8", "www.facebook.com", "www.youtube.com"}


def serverInteraction(map):
	response = ""
	i = 0
	while i < 5:
		if len(map) != 0:
			jsonData = json.dumps(map)
			print "JSON DATA: ",jsonData

			url = 'http://127.0.0.1:5000/pushSecondsData'
			response = requests.post(url, data=jsonData, headers={"Content-Type":"application/json"})
			response = response.json()

			print "Response: ", response
			if response['StatusCode'] == '200':
				break
			i += 1 
			print "Server status not 200"
		else:
			break;


def sendData(time, data, clientId):
	try:
		map = {}
		map["clientId"] = clientId
		map["data"] = data
		map["time"] = time
		print
		serverInteraction(map)
			
	except Exception as e:
		print "Error in sendData", str(e)


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
	#ip = getIp(me.edgemap)
	#print ip

	dataList = []
	fileIndex = str(randint(10,30))
	filename = "/home/vipra/ProjectReport2/dataset/" + fileIndex + "_dataset.txt";
	print filename
	file = open(filename, 'r')
	
	for line in file:
		line = line.strip('\n')
		dataList.append(line)

	i = 0
	while True:
		now = datetime.datetime.now()
		try:
			sendData(str(now), dataList[i], me.clientId)
		except Exception as e:
			print "Retrying..."

		print "data sent", i
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