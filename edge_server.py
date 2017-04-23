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



	def __pushData(self, date, hour, minute):
		#print "INSIDE __PUSH DATA"
		print "date: ", date
		dic = {}
		dic["bp"] = self.__getBp()
		dic["steps"] = self.__stepsCounter
		dic["pulse"] = self.__getAveragePulse()

		if date in self.__master:
			timeDict = self.__master[date]
			if hour in timeDict:
				minuteDict = timeDict[hour]
			else:
				minuteDict = {}
		else:
			timeDict = {}
			minuteDict = {}
		
		minuteDict[minute] = dic
		timeDict[hour] = minuteDict
		
		self.__master[date] = timeDict
		print "timeDict: ", timeDict
		print self.__master[date]



	def addDataToMap(self, dataMap):
		
		datetm = self.__convertStrToDate(clientDT)
		date = datetm.date()

		newData = dataMap["data"]
		newTime = dataMap["time"]
		clientData = self.master[dataMap["clientId"][date][datetm.hour]]

		steps = int(clientData["steps"]) + int(newData["steps"])
		distance = int(clientData["distance"]) + int(newData["distance"])
		elevation = int(clientData["elevation"]) + int(newData["elevation"])
		calories = int(clientData["calories"]) + int(newData["calories"])
		floors = int(clientData["floors"])+ int(newData["floors"])

		pulse = self.__getAveragePulse(int(clientData["pulse"]) + int(newData["pulse"]), int(clientData["num"]))
		bp = self.__getBp(int(clientData["bp"]), int(newData["bp"]), int(newData["num"]))

		clientData["steps"] = steps
		clientData["distance"] = distance
		clientData["elevation"] = elevation
		clientData["calories"] = calories
		clientData["floors"] = floors
		clientData["pulse"] = pulse
		clientData["bp"] = bp
		clientData["num"] = str(int(clientData["bp"]) + 1)

		self.master[dataMap["clientId"]][date][datetm.hour] = clientData


	def addNewClientToMap(self, dataMap):
		datetm = self.__convertStrToDate(clientDT)
		date = datetm.date()

		newData = dataMap["data"]
		newTime = dataMap["time"]
		#clientData = self.master[dataMap["clientId"][date][datetm.hour]]

		steps = int(newData["steps"])
		distance = int(newData["distance"])
		elevation = int(newData["elevation"])
		calories =int(newData["calories"])
		floors = int(newData["floors"])

		pulse = int(newData["pulse"])
		bp = newData["bp"]


		clientData["steps"] = steps
		clientData["distance"] = distance
		clientData["elevation"] = elevation
		clientData["calories"] = calories
		clientData["floors"] = floors
		clientData["pulse"] = pulse
		clientData["bp"] = bp
		clientData["num"] = 1

		self.master[dataMap["clientId"]][date][datetm.hour] = clientData


	def incrementCounters(self, dataMap):
		#2014-09-26 16:34:40.278298
		
		datetm = self.__convertStrToDate(clientDT)
		date = datetm.date()
		if dataMap["clientId"][date][datetm.hour] in self.master:
			self.addDataToMap(dataMap)
		elif dataMap["clientId"][date] in self.master:
			#TODO
		elif dataMap["clientId"] in self.master:
			#TODO
		else:
			self.addNewClientToMap(dataMap)

		'''
		if self.__currentDate == 0:
			self.__setClassDateTime(clientDT)
		else :
			if (self.__currentDate != date or self.__currentHour != datetm.hour or self.__currentMinute != datetm.minute):
				self.__pushData(str(self.__currentDate), self.__currentHour, self.__currentMinute)
				self.__resetCounters()
				self.__setClassDateTime(clientDT)
		print self.__currentDate, date, self.__currentHour, datetm.hour, self.__currentMinute, datetm.minute
		self.__bpSysCounter += int(bpSys)
		self.__bpDysCounter += int(bpDys)
		self.__stepsCounter += int(steps)
		self.__pulseCounter += int(pulse)
		self.__num += 1
		'''
		return "Done"


'''
	def __setClassDateTime(self, clientDT):
		#print "Inside __setClassDateTime"
		datetm = self.__convertStrToDate(clientDT)
		date = datetm.date()
		
		if self.__currentDate != date: 
			self.__currentDate = date
			self.__currentHour = datetm.hour
			self.__currentMinute = datetm.minute

		elif self.__currentHour != datetm.hour:
			self.__currentHour = datetm.hour
			self.__currentMinute = datetm.minute

		elif self.__currentMinute < datetm.minute:
			self.__currentMinute = datetm.minute
'''


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
