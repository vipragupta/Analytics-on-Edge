import datetime
import socket

class Counters():
	def __init__(self):
		self.master = {}
#		self.bpSysCounter = 0
#		self.bpDysCounter = 0
#		self.stepsCounter = 0
#		self.pulseCounter = 0
#		self.__currentMinute = 0
#		self.__currentHour = 0
#		self.__currentDate = 0
#sss		self.__num = 0


	def __resetCounters(self):
#		self.__bpSysCounter = 0
#		self.__bpDysCounter = 0
#		self.__stepsCounter = 0
#		self.__pulseCounter = 0
#		self.__num = 0


	def printDic(self):
		print self.__master


	def processData(self, oldDataMap, newData):
		map = {}
		map["steps"] = ((len(oldDataMap) == 0) ? 0 :int(oldDataMap["steps"])) + int(newData["steps"])
		map["distance"] = ((len(oldDataMap) == 0) ? 0 :int(oldDataMap["distance"])) + int(newData["distance"])
		map["elevation"] = ((len(oldDataMap) == 0) ? 0 :int(oldDataMap["elevation"])) + int(newData["elevation"])
		map["calories"] = ((len(oldDataMap) == 0) ? 0 :int(oldDataMap["calories"])) + int(newData["calories"])
		map["floors"] = ((len(oldDataMap) == 0) ? 0 :int(oldDataMap["floors"]))+ int(newData["floors"])

		map["pulse"] = self.__getAveragePulse(((len(oldDataMap) == 0) ? 0 :int(oldDataMap["pulse"])) + int(newData["pulse"]), int(oldDataMap["num"]))
		map["bp"] = self.__getBp(((len(oldDataMap) == 0) ? 0 : int(oldDataMap["bp"])), int(newData["bp"]), ((len(oldDataMap) == 0) ? 1 : int(oldDataMap["num"])))

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



	def incrementCounters(self, dataMap):
		
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



def extractData(str):
	map = {}

	dataMap = {'distance': 0, 'elevation': 0, 'calories': 18.556499481201172, 'pulse': '135', 'floors': 0, 'bp': '130/54', 'steps': 0}
	map["data"] = dataMap
	map["clientId"] = "784512"
	map["time"]	= str(now)

	return map 			#TODO


if __name__ == '__main__':

    count = Counters()
    #port = raw_input("Enter a port to start on: ")

    try:
        while True:
        #    print ("waiting for request ...")
        #    request, client  = sock.recvfrom(10240)
        #    print "request:", request
            dataMap = extractData(request)

        #    clientDT = data[0]
        #    steps = data[2]
        #    pulse = data[1]
        #    bpsys = data[3].split('/')[0]
        #    bpdys = data[3].split('/')[1]

            sendMessage = count.incrementCounters(dataMap) 								# where all the operations happen
            if sendMessage == None:
                sendMessage = ""

            #print("sendMessage: ", sendMessage)
            count.printDic()
            #time.sleep(0.9)     #as server sync msg comes after the menu has printed. i.e. the server output is slow
            
            send = sock.sendto(sendMessage, client)
            
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
