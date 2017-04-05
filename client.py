from random import randint
import time
import datetime
import socket
import requests

def generateBP():
	num = randint(0,1)
	if num == 1:
		systolic = str(num) + str(randint(0,9)) + str(randint(0,9))
	else :
		systolic = str(randint(7,9)) + str(randint(0,9))

	diastolic = str(randint(0,9)) + str(randint(0,9))
	return systolic + "/" + diastolic

def generateSteps():
	steps = str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9))
	return steps

def generatePulse():
	num = randint(0,2)
	if num == 0:
		beat = str(randint(8,9)) + str(randint(0,9))
	elif num == 1 :
		beat = str(num) + str(randint(0,9)) + str(randint(0,9))
	else :
		beat = 200

	return beat


def serverInteraction(data, address, port, tries):
	response = ""

	if data != "":
		while (True):
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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


def sendData(time, bp, steps, pulse, address, port, i):

	task = str(time) + "#" + str(bp) + "#" + str(steps) + "#" + str(pulse) + "#" + str(i)
	try:
		
		print
		print "Request's Data:", task
		serverInteraction(task, address, port, 1)
			
	except socket.error, msg:
		print ("Error during sending message.")
		print ("ERROR CODE: ", msg[0])
		print ("ERROR MESSAGE: ", msg[1])



if __name__ == '__main__':
	i = 1000
	address = "127.0.0.1"
	port = raw_input("Enter a port to send: ")	
	while (i > 0):
		now = datetime.datetime.now()
		sendData(str(now), generatePulse(), generateSteps(), generateBP(), address, port, i)
		time.sleep(1)
		i -=1