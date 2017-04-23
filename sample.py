import webbrowser
import sys
import os
import requests
from flask import Flask
import json


graphMenuDict = {1:"distance", 2:"elevation", 3:"calories", 4:"pulse", 5:"floors", 6:"bp", 7:"steps"}
durationMenuDict = {1:"daily", 2:"weekly", 3:"monthly", 4:"yearly"}

#----------------------------------userMenu-------------------------------------
def userMenu(clientId):
    try:
        mainMenuChoice = 0
        while(mainMenuChoice != 3):
            mainMenu = "======USER MENU======\n1. View Today's summary\n2. Generate Graphs\n3. Close the Application\n"
            print mainMenu
            print "Enter your choice: "
            mainMenuChoice = int(input())

            if(mainMenuChoice == 1):
                createJsonData(mainMenuChoice, 0, clientId)
                #displayTodaySummary(mainMenuChoice, clientId)

            elif(mainMenuChoice == 2):
                graphMenu = "\n======GRAPH MENU======\n1. Distance\n2. Elevation\n3. Calories\n4. Pulse\n5. Floors\n6. Blood Pressure\n7. Steps\n"
                print graphMenu
                print "Which graph do you want to generate?: "
                graphMenuChoice = int(input())

                durationMenu = "\n======DURATION MENU======\n1. Daily\n2. Weekly\n3. Monthly\n4. Yearly\n"
                print durationMenu
                print "Please select the time-frame for graph: "
                durationMenuChoice = int(input())

                if((graphMenuChoice >= 1 and graphMenuChoice <=7) and (durationMenuChoice >=1 and durationMenuChoice <= 4)):
                    createJsonData(graphMenuChoice, durationMenuChoice, clientId)
                    #displayGraph(graphMenuChoice, durationMenuChoice, clientId)
                else:
                    print "Wrong Choice!"

            elif(mainMenuChoice == 3):
                print "Goodbye!"

            else:
                print "Wrong Choice!"

    except:
		comment = ('EXCEPTION: ' + str(sys.exc_info()[1]))
		print comment
		return 0

#--------------------------------createJSONData---------------------------------
def createJsonData(graphMenuChoice, durationMenuChoice, clientId):
    if(durationMenuChoice == 0):
        data = {"clientId":clientId}
    else:
        data = {"clientId":clientId, "type":graphMenuDict[graphMenuChoice], "duration":durationMenuDict[durationMenuChoice]}
    data = json.dumps(data)
    print data

    #url = 'http://ES_search_demo.com/document/record/_search?pretty=true'
    #response = requests.post(url, data=data)


#--------------------------------performOperation-------------------------------
def displayTodaySummary(mainMenuChoice, clientId):
    print mainMenuChoice


#--------------------------------performOperation-------------------------------
#@app.route('/some-url')
def displayGraph(graphMenuChoice, durationMenuChoice, clientId):
    print "Your graphMenuChoice: " + str(graphMenuChoice)
    print "Your durationMenuChoice: " + str(durationMenuChoice)


#---------------------------------HTMLReport------------------------------------
def htmlReport():
	try:
		reportName = "heartbeat"
		clientID = "100100"
		avgHeartBeat = 80

		# Create the HTML file for output
		htmlReportPath = os.path.dirname(os.path.realpath(__file__))
		htmlReportPath = os.path.join(htmlReportPath,"report.html")
		print htmlReportPath
		htmlReportFp = open(htmlReportPath,"w")

		# write html document
		global html
		html = """
		<!DOCTYPE html>
		<html>
		<head>
			<title>Sample Report</title>
			<style>
			.wrapper  {
				width: 100%;
				height: 100%;
				background-color: #FFF;
				cursor: default;
			}

			.report {
				font-family: Arial;
				font-size: 10px;
				border-width: 1px;
				border-spacing: 1px;
				border-style: outset;
				border-color: gray;
				border-collapse: separate;
				padding: 0px;
				background: #FFF;
			}

			.report tr:hover {
				background-color: #DBDBFF;
			}

			.heading {
				font-family: Arial;
				font-size: 18px;
				font-weight: 900;
				padding: 50px;
				color: #3399FF;
				margin-left: 20px;
			}

			.report th {
				background: #59ACFF;
				color: white;
			}

			.report td,th{
				border-width: 0.5px;
				border-style: inset;
				border-color: white;
				border-collapse: collapse;
				padding: 10px;
			}

			.logo {
				width: 130px;
				height: 100px;
				float: left;
				padding: 30px;
			}

			.caption {
				font-family: Arial;
				font-size: 14px;
				font-weight: 900;
				padding: 10px;
			}
			</style>
		</head>

		<body class="main">
		<header>
			<h1 class="heading">Report: """ + reportName + """ Client ID: """ + clientID + """</h1>
			<h3 class="caption"> Average """ + reportName + """: """ + str(avgHeartBeat) + """</h3>
		</header>
		<div class="wrapper">
			<p> Hello </p>
		<br/>
		"""

		htmlReportFp.write(html)

		# write all closing tags
		htmlReportFp.write('</div>')
		htmlReportFp.write('</body>')
		htmlReportFp.write('</html>')

		# print results to shell
		print "Created html report"
		htmlReportFp.close()

		webbrowser.get().open(htmlReportPath)

		return 0

	except:
		comment = ('EXCEPTION: ' + str(sys.exc_info()[1]))
		print comment
		return 0

if __name__ == '__main__':
    clientId = raw_input("Please enter your ID: ")
    print clientId
    userMenu(clientId)
    #htmlReport()