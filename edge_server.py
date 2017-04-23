import datetime
import socket

class Edge():

	def __init__(self):
		self.master        = {}
		self.localSummary  = {}
		self.clientSummary = {}


	def checkResetData(self):
		datetm = datetime.datetime.strptime(str(now), "%Y-%m-%d %H:%M:%S.%f")
		if datetm.hour == 00 && datetm.minute == 00 && datatm.second > 0		#Reset all data at 00:05
			self.master        = {}
			self.localSummary  = {}
			self.clientSummary = {}


	def printDic(self):
		print self.__master


	def __getMinutesActive(self, current, new):
		current = current + new
		return str(current)


	def __processClientSummary(self, newData):
		map = processData(self.clientSummary, newData)
		
		self.clientSummary["steps"]     = map["steps"]
		self.clientSummary["distance"]  = map["distance"]
		self.clientSummary["elevation"] = map["elevation"]
		self.clientSummary["calories"]  = map["calories"]
		self.clientSummary["floors"]    = map["floors"]
		self.clientSummary["active"]    = map["active"]
		self.clientSummary["pulse"]     = map["pulse"]
		self.clientSummary["bp"]        = map["bp"]


	def __processLocalSummary(self, newData):
		map = processData(self.localSummary, newData)
		num = ((len(oldDataMap) == 0) ? 1 : int(oldDataMap["num"]))

		self.localSummary["steps"]     = map["steps"]     / 
		self.localSummary["distance"]  = map["distance"]  / num
		self.localSummary["elevation"] = map["elevation"] / num
		self.localSummary["calories"]  = map["calories"]  / num
		self.localSummary["floors"]    = map["floors"]    / num
		self.localSummary["active"]    = map["active"]    / num
		self.localSummary["pulse"]     = map["pulse"]
		self.localSummary["bp"]        = map["bp"]


	def processData(self, oldDataMap, newData):
		map = {}
		num = ((len(oldDataMap) == 0) ? 1 : int(oldDataMap["num"]))

		if newData["steps"] > 0:
			newData["active"] = 30
		elif:
			newData["active"] = 0

		map["steps"]     = ((len(oldDataMap) == 0) ? 0 :int(oldDataMap["steps"]))     + int(newData["steps"])
		map["distance"]  = ((len(oldDataMap) == 0) ? 0 :int(oldDataMap["distance"]))  + int(newData["distance"])
		map["elevation"] = ((len(oldDataMap) == 0) ? 0 :int(oldDataMap["elevation"])) + int(newData["elevation"])
		map["calories"]  = ((len(oldDataMap) == 0) ? 0 :int(oldDataMap["calories"]))  + int(newData["calories"])
		map["floors"]    = ((len(oldDataMap) == 0) ? 0 :int(oldDataMap["floors"]))    + int(newData["floors"])
		
		map["active"]= self.__getSecondsActive(((len(oldDataMap) == 0) ? 0 : int(oldDataMap["active"])), int(newData["active"]))

		map["pulse"] = self.__getAveragePulse(((len(oldDataMap) == 0)  ? 0 : int(oldDataMap["pulse"])) + int(newData["pulse"]), num)
		map["bp"]    = self.__getBp(((len(oldDataMap) == 0)            ? 0 : int(oldDataMap["bp"])), int(newData["bp"]), num)

		return map



	# Add data when client's that hour data is present also.
	def addDataToExisitngHour(self, dataMap, datetm):
		map = processData(self.master[dataMap["clientId"][datetm.date()][datetm.hour]], dataMap)
		clientData = map
		clientData["num"] = str(int(clientData["num"]) + 1)
		self.master[dataMap["clientId"]][date][datetm.hour] = clientData



	# Add data when client Data is present on edge for the given date, but it doesn't contain that hour data
	def addDataToExisitingDate(self, dataMap, datatm):
		clientData = processData({}, dataMap)
		clientData["num"] = str(int(clientData["num"]) + 1)
		map1 = {datetm.hour: clientData}
		self.master[dataMap["clientId"]][datetm.date()] = map1



	# Add data when client Data is present on edge for the given date, but it doesn't contain that hour data
	def addDataToExisitingClient(self, dataMap, datatm):
		clientData = processData({}, dataMap)
		clientData["num"] = str(int(clientData["num"]) + 1)
		map1 = {datetm.hour: clientData}
		map2 = {datetm.date(): map1}
		self.master[dataMap["clientId"]] = map2



	# Add data when client Data is not present also.
	def addData(self, dataMap, datatm):
		clientData = processData({}, dataMap)
		clientData["num"] = str(int(clientData["num"]) + 1)
		map1 = {datetm.hour: clientData}
		map2 = {datetm.date(): map1}
		self.master[dataMap["clientId"]] = map2



	def __incrementCounters(self, dataMap):
		datetm = self.__convertStrToDate(dataMap["time"])
		date = datetm.date()
		if dataMap["clientId"][date][datetm.hour] in self.master:
			self.addDataToMap(dataMap, datetm)
		elif dataMap["clientId"][date] in self.master:
			self.addDataToExisitingDate(dataMap, datetm)
		elif dataMap["clientId"] in self.master:
			addDataToExisitingClient(dataMap, datetm)
		else:
			self.addData(dataMap, datetm)
		return "Done"



	def __convertStrToDate(self, date):
		return datetime.datetime.strptime(clientDT, "%Y-%m-%d %H:%M:%S.%f")


	def __getAveragePulse(self):
		return pulse/num


	def __getBp(self, currentBp, newBp, num):

		currentsys = currentBp.split('/')[0]
        currestdys = currentBp.split('/')[1]

        newsys = newBp.split('/')[0]
        newdys = newBp.split('/')[1]

		sys = (currentsys + newsys)/num
		dys = (currentdys + newdys)/num

		return str(sys) + "/" + str(dys)

	def processData(self, dataMap):
		self.__incrementCounters(dataMap)
		self.__processClientSummary(newData)
		self.__processLocalSummary(newData)


def extractData(str):
	map = {}
	clientId = ["8745274174", "8674587532", "7946547861"]
	dataMap = {'distance': random.uniform(0, 1.0), 'elevation': random.uniform(0, 2.0),
				'calories': random.uniform(0, 20.0), 'pulse': randint(60, 120), 'floors': random.uniform(0, 2.0), 'bp': '130/54', 'steps': randint(0,30)}
	map["data"] = dataMap
	map["clientId"] = clientId[randint(0,3)]
	map["time"]	= str(now)

	return map 			#TODO


if __name__ == '__main__':

    edge = Edge()

    try:
        while True:
            dataMap = extractData(request)
            sendMessage = edge.processData(dataMap) 								# where all the operations happen
            
            if sendMessage == None:
                sendMessage = ""

            #print("sendMessage: ", sendMessage)
            edge.printDic()
            edge.checkResetData()
            #send = sock.sendto(sendMessage, client)
            
            print
            print

    except socket.error, msg:
        print ("Error during sending message.")
        print ("ERROR CODE: ", msg[0])
        print ("ERROR MESSAGE: ", msg[1])

    finally:
        print ("closing socket")
        sock.close()
'''
{	"userId" : {
		"04032017":{
					"0" :{
								"bp" : 123/78,			//average
								"steps" : 123456,	//total
								"pulse" : 98		//average
								}, 
					"1" : {
								"bp" : 123,			//average
								"steps" : 123456,	//total
								"pulse" : 98		//average
								}
					},
		"04042017":{
					"0" :{
								"bp" : 123/78,			//average
								"steps" : 123456,	//total
								"pulse" : 98		//average
								}, 
					"1" : {
								"bp" : 123,			//average
								"steps" : 123456,	//total
								"pulse" : 98		//average
								}
					},
	}
}
'''
