import datetime
import socket

class Counters():
	def __init__(self):
		self.__master = {}
		self.__bpSysCounter = 0
		self.__bpDysCounter = 0
		self.__stepsCounter = 0
		self.__pulseCounter = 0
		self.__currentMinute = 0
		self.__currentHour = 0
		self.__currentDate = 0
		self.__num = 0


	def __resetCounters(self):
		self.__bpSysCounter = 0
		self.__bpDysCounter = 0
		self.__stepsCounter = 0
		self.__pulseCounter = 0
		self.__num = 0


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


	def incrementCounters(self, bpSys, bpDys, steps, pulse, clientDT):
		#2014-09-26 16:34:40.278298
		datetm = self.__convertStrToDate(clientDT)
		date = datetm.date()

		#print self.__currentDate, date, self.__currentHour, datetm.hour, self.__currentMinute, datetm.minute
		#print self.__currentDate == date, self.__currentHour == datetm.hour, self.__currentMinute == datetm.minute

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
		return "Done"


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


	def __convertStrToDate(self, date):
		return datetime.datetime.strptime(clientDT, "%Y-%m-%d %H:%M:%S.%f")


	def __getAveragePulse(self):
		if self.__num != 0:
			return self.__pulseCounter/self.__num
		return self.__pulseCounter

	def __getBp(self):
		if self.__num != 0:
			sys = self.__bpSysCounter/self.__num
			dys = self.__bpDysCounter/self.__num
		else:
			sys = self.__bpSysCounter
			dys = self.__bpDysCounter
		return str(sys) + "/" + str(dys)



def extractData(str):
	return str.split('#')


if __name__ == '__main__':

    count = Counters()
    port = raw_input("Enter a port to start on: ")

    try: 
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("127.0.0.1", int(port)))

        while True:
            print ("waiting for request ...")
            request, client  = sock.recvfrom(10240)
            print "request:", request
            data = extractData(request)

            clientDT = data[0]
            steps = data[2]
            pulse = data[1]
            bpsys = data[3].split('/')[0]
            bpdys = data[3].split('/')[1]

            sendMessage = count.incrementCounters(bpsys, bpdys, steps, pulse, clientDT) # where all the operations happen
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
					"0000" :{
							"00" : {
								"bp" : 123/78,			//average
								"steps" : 123456,	//total
								"pulse" : 98		//average
								}, 
							"01" : {
								"bp" : 123,			//average
								"steps" : 123456,	//total
								"pulse" : 98		//average
								} 
							} , 
					"0100" : {
							"00" : {
								"bp" : 123,			//average
								"steps" : 123456,	//total
								"pulse" : 98		//average
								}, 
							"01" : {
								"bp" : 123,			//average
								"steps" : 123456,	//total
								"pulse" : 98		//average
								}
						}
					},
		"04042017":{
					"0000" :{
							"00" : {
								"bp" : 123,			//average
								"steps" : 123456,	//total
								"pulse" : 98		//average
								}, 
							"01" : {
								"bp" : 123,			//average
								"steps" : 123456,	//total
								"pulse" : 98		//average
								} 
							} , 
					"0100" : {
							"00" : {
								"bp" : 123,			//average
								"steps" : 123456,	//total
								"pulse" : 98		//average
								}, 
							"01" : {
								"bp" : 123,			//average
								"steps" : 123456,	//total
								"pulse" : 98		//average
								}
						}
					}
	}
}
'''
