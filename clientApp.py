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


graphMenuDict = {1:"distance", 2:"elevation", 3:"calories", 4:"pulse", 5:"floors", 6:"bp", 7:"steps"}
durationMenuDict = {0:"dailyall",1:"daily", 2:"weekly", 3:"monthly", 4:"yearly"}
todayDate = str(datetime.datetime.now().date())

#----------------------------------userMenu-------------------------------------
def userMenu(clientId):
    try:
        mainMenu = "======USER MENU======\n1. View Today's summary\n2. Generate Graphs\n3. Close the Application\n"
        print mainMenu
        print "Enter your choice: "
        mainMenuChoice = int(input())

        if(mainMenuChoice == 1):
            createJsonData(mainMenuChoice, 0, clientId)

        elif(mainMenuChoice == 2):
            graphMenu = "\n======GRAPH MENU======\n1. Distance\n2. Elevation\n3. Calories\n4. Pulse\n5. Floors\n6. Blood Pressure\n7. Steps\n"
            print graphMenu
            print "Which graph do you want to generate?: "
            graphMenuChoice = int(input())

            durationMenu = "\n======DURATION MENU======\n1. Stats for the Day\n2. Stats for the Week\n3. Stats for the Month\n4. Stats for the Year\n"
            print durationMenu
            print "Please select the time-frame for graph: "
            durationMenuChoice = int(input())

            if((graphMenuChoice >= 1 and graphMenuChoice <=7) and (durationMenuChoice >=1 and durationMenuChoice <= 4)):
                createJsonData(graphMenuChoice, durationMenuChoice, clientId)
                #displayGraph(graphMenuChoice, durationMenuChoice, clientId)
            else:
                print "Wrong Choice!"

        else:
            print "Wrong Choice!"

    except:
		comment = ('EXCEPTION: ' + str(sys.exc_info()[1]))
		print comment
		return 0

#--------------------------------createJSONData---------------------------------
def createJsonData(graphMenuChoice, durationMenuChoice, clientId):
    if(durationMenuChoice == 0):
        data = {'clientId':clientId,'duration':durationMenuDict[durationMenuChoice],"date":todayDate}
    else:
        data = {'clientId':clientId,'type':graphMenuDict[graphMenuChoice],'duration':durationMenuDict[durationMenuChoice],"date":todayDate}
    jsonData = json.dumps(data)
    print jsonData

    url = 'http://localhost:5000/post'
    response = requests.post(url, data=jsonData, headers={"Content-Type":"application/json"})
    response = response.json()
    #print response
##    del response['Message']
##    del response['StatusCode']
##    temp = response.keys()
##    keys = []
##    for i in dummy:
##        keys.append(int(i))
##    keys.sort()
##    print keys

    displayGraph(data,response)


#------------------------------------MAIN---------------------------------------
if __name__ == '__main__':
    clientId = raw_input("Please enter your ID: ")
    print clientId
    userMenu(clientId)