import webbrowser
import sys
import os
from flask import Flask, jsonify, request
import requests
import json
import datetime


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
    displayGraph(data,response)


#-------------------Generate Graph and create HTML Report-----------------------
def displayGraph(data,result):
    print result
    try:
        if(data['duration'] == "dailyall"):
            reportName = "Summary for today"
            print reportName
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
            <!-- Resources -->
            <script src="https://www.amcharts.com/lib/3/amcharts.js"></script>
            <script src="https://www.amcharts.com/lib/3/serial.js"></script>
            <script src="https://www.amcharts.com/lib/3/plugins/export/export.min.js"></script>
            <link rel="stylesheet" href="https://www.amcharts.com/lib/3/plugins/export/export.css" type="text/css" media="all" />
            <script src="https://www.amcharts.com/lib/3/themes/none.js"></script>
            <link href="https://fonts.googleapis.com/css?family=Lato:300" rel="stylesheet">

            <!-- Chart code -->
            <script>
            var chart = AmCharts.makeChart("chartdiv", {
                "theme": "none",
                "type": "serial",
            	"startDuration": 2,
                "dataProvider": [{
                    "country": "Distance",
                    "visits": """ + result['distance'] + """,
                    "color": "#FF0F00"
                }, {
                    "country": "Elevation",
                    "visits": """ + result['elevation'] + """,
                    "color": "#FF6600"
                }, {
                    "country": "Hour",
                    "visits": """ + result['hour'] + """,
                    "color": "#FF9E01"
                }, {
                    "country": "Pulse",
                    "visits": """ + result['pulse'] + """,
                    "color": "#FCD202"
                }, {
                    "country": "Floors",
                    "visits": """ + result['floors'] + """,
                    "color": "#F8FF01"
                }, {
                    "country": "Blood Pressure",
                    "visits": """ + result['bp'] + """,
                    "color": "#B0DE09"
                }, {
                    "country": "Active Hours",
                    "visits": """ + result['active'] + """,
                    "color": "#04D215"
                }, {
                    "country": "Steps",
                    "visits": """ + result['steps'] + """,
                    "color": "#0D8ECF"
                }],

                "valueAxes": [{
                    "position": "left",
                    "title": "Count"
                }],
                "graphs": [{
                    "balloonText": "[[category]]: <b>[[value]]</b>",
                    "fillColorsField": "color",
                    "fillAlphas": 0.75,
                    "lineAlpha": 0.1,
                    "type": "column",
                    "valueField": "visits"
                }],
                "depth3D": 20,
            	"angle": 30,
                "chartCursor": {
                    "categoryBalloonEnabled": false,
                    "cursorAlpha": 0,
                    "zoomable": false
                },
                "categoryField": "country",
                "categoryAxis": {
                    "gridPosition": "start",
                    "labelRotation": 40
                },
                "export": {
                	"enabled": true
                 }

            });
            </script>

        <head>
			<title>Report</title>
			<style>
                #chartdiv {
                    position: absolute;
                    margin: auto;
                    top: 0;
                    right: 0;
                    bottom: 0;
                    left: 0;
                    width: 80%;
                    height: 430px;

                }

                .heading{
                    color: #111;
                    font-family: 'Lato', sans-serif;
                    font-size: 40px;
                    font-weight: bold;
                    letter-spacing: -1px;
                    line-height: 1;
                    text-align: center;
                }
			</style>
		</head>

		<body class="main">
		<header>
			<h1 class="heading">Report: """ + reportName + """</h1>
		</header>
		<div id="chartdiv"></div>
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

    except:
		comment = ('EXCEPTION: ' + str(sys.exc_info()[1]))
		print comment
		return 0

if __name__ == '__main__':
    clientId = raw_input("Please enter your ID: ")
    print clientId
    userMenu(clientId)