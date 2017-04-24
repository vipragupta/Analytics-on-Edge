import datetime
import time
import random
from datetime import datetime
from random import randint
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import json
import requests
import json
import ast

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SERVER_NAME='10.0.0.237:5000'
)
api = Api (app)


class Edge():

	def __init__(self):
		self.ip = "8.8.8.8"
		self.master        = {}
		self.localSummary  = {}
		self.clientSummary = {}


	def checkResetData(self):
		now = datetime.now()
		datetm = datetime.strptime(str(now), "%Y-%m-%d %H:%M:%S.%f")
		if datetm.hour == 00 and datetm.minute == 00 and datatm.second > 0:		#Reset all data at 00:05
			self.master        = {}
			self.localSummary  = {}
			self.clientSummary = {}


	def printDic(self):
		print
		for id in self.master:
			print id, ": ", self.master[id]
		print
		print "CLIENT SUMMARY: ",self.clientSummary
		print
		print "LOCAL SUMMARY: ",self.localSummary


	def __getMinutesActive(self, current, new):
		current = current + new
		return str(current)


	def __processClientSummary(self, newData):
		data = ast.literal_eval(newData["data"])
		clientSum = self.clientSummary[newData["clientId"]] if newData["clientId"] in self.clientSummary else {}
		map = self.__processData(clientSum, data)
		if len(map) > 0:
			clientSum["steps"]     = map["steps"]
			clientSum["distance"]  = map["distance"]
			clientSum["elevation"] = map["elevation"]
			clientSum["calories"]  = map["calories"]
			clientSum["floors"]    = map["floors"]
			clientSum["active"]    = map["active"]
			clientSum["pulse"]     = map["pulse"]
			clientSum["bp"]        = map["bp"]
			clientSum["num"]       = map["num"]
			self.clientSummary[newData["clientId"]] = clientSum


	def __processLocalSummary(self, newData):
		data = ast.literal_eval(newData["data"])
		map = self.__processData(self.localSummary, data)
		if len(map) > 0:
			num = int(map["num"])

			self.localSummary["steps"]     = str(int(map["steps"])       / 2)
			self.localSummary["distance"]  = str(float(map["distance"])  / 2)
			self.localSummary["elevation"] = str(float(map["elevation"]) / 2)
			self.localSummary["calories"]  = str(float(map["calories"])  / 2)
			self.localSummary["floors"]    = str(float(map["floors"])    / 2)
			self.localSummary["active"]    = str(float(map["active"])    / 2)
			self.localSummary["pulse"]     = map["pulse"]
			self.localSummary["bp"]        = map["bp"]
			self.localSummary["num"]       = map["num"]

	def __processData(self, oldDataMap, newData):
		try:
			map = {}
			num = (1 if (len(oldDataMap) == 0) else int(oldDataMap["num"])+1)
			
			if int(newData['steps']) > 0:
				newData["active"] = "30"
			else:
				newData["active"] = "0"

			map["steps"]     = ("0" if (len(oldDataMap) == 0) else str(int(oldDataMap["steps"]) + int(newData["steps"])))
			map["distance"]  = ("0" if (len(oldDataMap) == 0) else str(float(oldDataMap["distance"])  + float(newData["distance"])))
			map["elevation"] = ("0" if (len(oldDataMap) == 0) else str(float(oldDataMap["elevation"]) + float(newData["elevation"])))
			map["calories"]  = ("0" if (len(oldDataMap) == 0) else str(float(oldDataMap["calories"])  + float(newData["calories"])))
			map["floors"]    = ("0" if (len(oldDataMap) == 0) else str(float(oldDataMap["floors"])    + float(newData["floors"])))
			
			map["active"]= ("0" if (len(oldDataMap) == 0) else str(float(oldDataMap["active"]) + float(newData["active"])))
			map["pulse"] = self.__getAveragePulse((0 if (len(oldDataMap) == 0) else int(oldDataMap["pulse"])) + int(newData["pulse"]), 2)
			map["bp"]    = self.__getBp(("0" if (len(oldDataMap) == 0) else oldDataMap["bp"]), newData["bp"], 2)
			map["num"] = str(num)
			return map
		except Exception as e:
			print "EXCEPTION", str(e)
			return {}



	# Add data when client's that hour data is present also.
	def addDataToExisitngHour(self, dataMap, datetm):
		data = ast.literal_eval(dataMap["data"])
		map = self.__processData(self.master[dataMap["clientId"]][self.getDate(datetm)][str(datetm.hour)], data)
		if len(map) > 0:
			self.master[dataMap["clientId"]][self.getDate(datetm)][str(datetm.hour)] = map



	# Add data when client Data is present on edge for the given date, but it doesn't contain that hour data
	def addDataToExisitingDate(self, dataMap, datetm):
		data = ast.literal_eval(dataMap["data"])
		clientData = self.__processData({}, data)
		if len(clientData) > 0:
			clientData["num"] = "1"
			map1 = {str(datetm.hour): clientData}
			self.master[dataMap["clientId"]][self.getDate(datetm)] = map1



	# Add data when client Data is present on edge for the given date, but it doesn't contain that hour data
	def addDataToExisitingClient(self, dataMap, datetm):
		data = ast.literal_eval(dataMap["data"])
		clientData = self.__processData({}, data)
		if len(clientData) > 0:
			clientData["num"] = "1"

			map1 = {str(datetm.hour): clientData}
			map2 = {self.getDate(datetm): map1}
			self.master[dataMap["clientId"]] = map2


	# Add data when client Data is not present also.
	def addData(self, dataMap, datetm):
		data = ast.literal_eval(dataMap["data"])
		clientData = self.__processData({}, data)
		if len(clientData) > 0:
			clientData["num"] = "1"
			map1 = {str(datetm.hour): clientData}
			map2 = {self.getDate(datetm): map1}
			self.master[dataMap["clientId"]] = map2



	def __incrementCounters(self, dataMap):
		datetm = self.__convertStrToDate(dataMap["time"])
		date = self.getDate(datetm)
		hour = str(datetm.hour)

		if (dataMap["clientId"] in self.master) and (date in self.master[dataMap["clientId"]]) and (hour in self.master[dataMap["clientId"]][date]):
			#print "************"			
			self.addDataToExisitngHour(dataMap, datetm)
		
		elif (dataMap["clientId"] in self.master) and (date in self.master[dataMap["clientId"]][date]) :
			#print "#####################"
			self.addDataToExisitingDate(dataMap, datetm)
		
		elif dataMap["clientId"] in self.master:
			#print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
			self.addDataToExisitingClient(dataMap, datetm)

		else:
			#print "$$$$$$$$$$$$$$$$$$$$$$$$$"
			self.addData(dataMap, datetm)

		return "Done"

	def getDate(self, datetm):
		stri = str(datetm.year)+ "-"+ str(datetm.month) +"-"+ str(datetm.day)
		return stri


	def __convertStrToDate(self, date):
		return datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")


	def __getAveragePulse(self, pulse, num):
		return str(pulse/num)


	def __getBp(self, currentBp, newBp, num):
		currentsys = 0 if currentBp == "0" else int(currentBp.split('/')[0])
		currestdys =  0 if currentBp == "0" else int(currentBp.split('/')[1])
		newsys = int(newBp.split('/')[0])
		newdys = int(newBp.split('/')[1])

		sys = (currentsys + newsys) / num
		dys = (currestdys + newdys) / num
		return str(sys) + "/" + str(dys)

	def processIt(self, dataMap):
		#data = ast.literal_eval(dataMap)
		self.__incrementCounters(dataMap)
		self.__processClientSummary(dataMap)
		self.__processLocalSummary(dataMap)


	def getServerData(self):
		finalList = {}
		
		client = {}
		now = datetime.now()
		datetm = datetime.strptime(str(now), "%Y-%m-%d %H:%M:%S.%f")
		date = self.getDate(datetm)
		
		if datetm.minute == 00:
			hour = str(int(datetm.hour) -1)
		else:
			hour = str(datetm.hour)

		finalList["clientSummary"] = self.clientSummary
		finalList["localSummary"] = self.localSummary
		
		for clientId in self.master:
			clientMap = {}
			if date in self.master[clientId]:
				dateMap = self.master[clientId][date]
				if hour in dateMap:
					clientMap = dateMap[hour]
					clientMap["hour"] = hour
					clientMap["date"] = date
			if len(clientMap) > 0:
				client[clientId] = clientMap

		finalList["hourly"] = client
		finalList["edge_ip"] = self.ip
		#print finalList
		return finalList

edge = Edge()

def extractData():
	map = {}
	clientId = ["8745274174", "8674587532", "7946547861"]
	dataMap = {'distance': str(random.uniform(0, 1.0)), 'elevation': str(random.uniform(0, 2.0)),
				'calories': str(random.uniform(0, 20.0)), 'pulse': str(randint(60, 120)),
				'floors': str(random.uniform(0, 2.0)), 'bp': '130/54', 'steps': str(randint(0,30))}
	map["data"] = dataMap
	map["clientId"] = clientId[randint(0,2)]
	now = datetime.now()
	map["time"]	= str(now)

	return map 			#TODO


def checkSendDataToCloud():

	now = datetime.now()
	datetm = datetime.strptime(str(now), "%Y-%m-%d %H:%M:%S.%f")
	if datetm.minute == 00 or datetm.minute == 30:		#Reset all data at 00:05
		return True
	else:
		return False


def serverInteraction(map):
	response = ""
	i = 0
	while i < 5:
		if len(map) != 0:
			jsonData = json.dumps(map)
			print "JSON DATA: ",jsonData

			url = 'http://52.41.73.23:5000/pushdata'
			response = requests.post(url, data=jsonData, headers={"Content-Type":"application/json"})
			response = response.json()

			print "Response: ", response
			if response['StatusCode'] == '200':
				break
			i += 1 
			print "Server status not 200"
		else:
			break;


@app.route('/pushSecondsData', methods=['GET', 'POST'])
def mypost():
	try:
		if(request.method == 'POST'):
			print "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
			print
			print
			print "Request: " , request.json
			#json1_data = json.loads()
			edge.processIt(request.json)
			edge.printDic()
			response = {'StatusCode':'200','Message':'Success'}
			response = json.dumps(response)

			if checkSendDataToCloud():
				print "Hi"
				dic = edge.getServerData()
				serverInteraction(dic)
			edge.checkResetData()
			return response
	
	except Exception as e:
		print "Error", str(e)
		response = {'StatusCode':'404','Message':'Fail'}
		response = json.dumps(response)
		return jsonify({'error': str(e)})




if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')