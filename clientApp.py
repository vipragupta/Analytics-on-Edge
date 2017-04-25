#-------------------------------------------------------------------------------
# Name:        clientApp
# Purpose:     An application interface for client
#
# Author:      Chaitra Ramachandra
#
# Created:     22/04/2017
# Copyright:   (c) chaitra 2017
#-------------------------------------------------------------------------------

import webbrowser
import sys
import os
from flask import Flask, jsonify, request
import requests
import json
import datetime
from generateReports import *
import timeit


graphMenuDict = {1:"distance", 2:"elevation", 3:"calories", 4:"pulse", 5:"floors", 6:"bp", 7:"steps"}
durationMenuDict = {0:"dailyall",1:"daily", 2:"weekly", 3:"yearly",4:"localAreaSummary"}
todayDate = str(datetime.datetime.now().date())
l = []


#-----------------------------GET NEAREST EDGE IP-------------------------------
#{"128.138.201.67", "10.0.0.237"}
def getEdgeIp(ipMap):
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




#----------------------------------USER MENU------------------------------------
def userMenu(clientId):
    mainMenuChoice = 0
    try:
        while(mainMenuChoice != 4):
            mainMenu = "======USER MENU======\n1. View Today's summary\n2. Generate Graphs\n3. Compare your performace with peers in your area?\n4. Close the Application\n"
            print mainMenu
            print "Enter your choice: "
            mainMenuChoice = int(input())
            #mainMenuChoice = 1

            if(mainMenuChoice == 1):
                createJsonData(mainMenuChoice, 0, clientId, 0)

            elif(mainMenuChoice == 2):
                graphMenu = "\n======GRAPH MENU======\n1. Distance\n2. Elevation\n3. Calories\n4. Pulse\n5. Floors\n6. Blood Pressure\n7. Steps\n"
                print graphMenu
                print "Which graph do you want to generate?: "
                graphMenuChoice = int(input())

                durationMenu = "\n======DURATION MENU======\n1. Stats for the Day\n2. Stats for the Week\n3. Stats for the Year\n"
                print durationMenu
                print "Please select the time-frame for graph: "
                durationMenuChoice = int(input())

                if((graphMenuChoice >= 1 and graphMenuChoice <=7) and (durationMenuChoice >=1 and durationMenuChoice <= 3)):
                    createJsonData(graphMenuChoice, durationMenuChoice, clientId, 0)
                else:
                    print "Wrong Choice!"

            elif(mainMenuChoice == 3):
                #edgeIp = getEdgeIp(clientId)
                edgeIp = "8.8.8.8"
                createJsonData(mainMenuChoice, 4, clientId, edgeIp)

            elif(mainMenuChoice == 4):
                print "Goodbye!"
                sys.exit("Client terminated the program")

            else:
                print "Wrong Choice!"

    except:
		comment = ('EXCEPTION: ' + str(sys.exc_info()[1]))
		print comment
		return 0



#---------------------------CREATE JSON DATA------------------------------------
def createJsonData(graphMenuChoice, durationMenuChoice, clientId, edgeIp):
    if(durationMenuChoice == 0):
        data = {'clientId':clientId,'duration':durationMenuDict[durationMenuChoice],"date":todayDate}

    elif(durationMenuChoice == 4): #for LocalAreaSummary
        data = {'clientId':clientId,'duration':durationMenuDict[durationMenuChoice],'type':durationMenuDict[durationMenuChoice],"date":todayDate,"ip":edgeIp}

    else:
        data = {'clientId':clientId,'type':graphMenuDict[graphMenuChoice],'duration':durationMenuDict[durationMenuChoice],"date":todayDate}

    jsonData = json.dumps(data)
    print jsonData

    url = 'http://localhost:5000/post'
    #url = 'http://34.223.200.168/getreport'

    start = timeit.default_timer()
    response = requests.post(url, data=jsonData, headers={"Content-Type":"application/json"},timeout = 10)
    end = timeit.default_timer()

    l.append(end-start)

    print response.json()

    if "200" in str(response):
        response = response.json()
        displayGraph(data,response)

    else:
        print str(response)
        print "Exiting the application!"




#-----------------------------ENTER CLIENT ID-----------------------------------
def enterClientId():
    clientId = str(raw_input("Please enter your ID: "))
    f = open('clientIds.txt', 'r')
    for eachline in f.readlines():
        if(clientId == eachline.strip()):
            print "Client ID " + clientId + " exists"
            return clientId

    print "Invalid Client ID! Please enter a valid ID!"
    return (None)




#------------------------------------MAIN---------------------------------------
if __name__ == '__main__':
    clientId = None
    while(clientId == None):
        clientId = enterClientId()

    userMenu(clientId)
##    for i in range(500):
##        clientId = "0000000000"
##        userMenu(clientId)
##
##    print "sum: ", sum(l)
