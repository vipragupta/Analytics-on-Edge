#-------------------------------------------------------------------------------
# Name:        generateReports
# Purpose:     This script will generate graphs for the client
#
# Author:      Chaitra Ramachandra
#
# Created:     23/04/2017
# Copyright:   (c) chaitra 2017
#-------------------------------------------------------------------------------

import webbrowser
import sys
import os
from flask import Flask, jsonify, request
import requests
import json
import datetime

#-------------------Generate Graph and create HTML Report-----------------------
def displayGraph(data,result):
    global html
    print result
    #Create the HTML file for output
    htmlReportPath = os.path.dirname(os.path.realpath(__file__))
    htmlReportPath = os.path.join(htmlReportPath,"report.html")
    htmlReportFp = open(htmlReportPath,"w")
    #print htmlReportPath

    try:
        if(data['duration'] == "dailyall"):
            reportName = "Summary for " + data['date']
            #bpList = (result['bp']).split("/")

        elif(data['duration'] == "daily"):
            reportName = "Hourly statistics of " + data['type'] + " for " + data['date']



        #write html document

        htmlResourcesSection = """
		<!DOCTYPE html>
		<html>
            <!-- Resources -->
            <script src="https://www.amcharts.com/lib/3/amcharts.js"></script>
            <script src="https://www.amcharts.com/lib/3/serial.js"></script>
            <script src="https://www.amcharts.com/lib/3/plugins/export/export.min.js"></script>
            <link rel="stylesheet" href="https://www.amcharts.com/lib/3/plugins/export/export.css" type="text/css" media="all" />
            <script src="https://www.amcharts.com/lib/3/themes/none.js"></script>
            <link href="https://fonts.googleapis.com/css?family=Lato:300" rel="stylesheet">
            <link rel="stylesheet" href="dailyAll.css" type="text/css"/>
        """

        htmlChartSection = """
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
                    "visits": """ + result['activemins'] + """,
                    "color": "#FF9E01"
                }, {
                    "country": "Pulse",
                    "visits": """ + result['calories'] + """,
                    "color": "#FCD202"
                }, {
                    "country": "Floors",
                    "visits": """ + result['pulse'] + """,
                    "color": "#F8FF01"
                }, {

                    "country": "Blood Pressure Systolic",
                    "visits": """ + bpList[0] + """,
                    "color": "#B0DE09"
                }, {

                    "country": "Blood Pressure Diastolic",
                    "visits": """ + bpList[1] + """,
                    "color": "#B0DE09"
                }, {
                    "country": "Active Hours",
                    "visits": """ + result['floors'] + """,
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
        """

        htmlHeadSection = """
        <head>
			<title>Report</title>
		</head>
        """

        htmlBodySectionForCharts = """
		<body class="main">
		<header>
			<h1 class="heading">Report: """ + reportName + """</h1>
		</header>
		<div id="chartdiv"></div>
        </body>
        </html>
		"""

        htmlBodySectionForDailyAll = """
        <body>
            <header>
                <h1 class="heading">Report: """ + reportName + """</h1>
            </header>
            <table class="table-fill">
                <thead>
                    <tr>
                        <th class="text-left">Activities</th>
                        <th class="text-left">Values</th>
                    </tr>
                </thead>
                <tbody class="table-hover">
                    <tr>
                        <td class="text-left">Distance</td>
                        <td class="text-left">""" + result['distance'] + """</td>
                    </tr>
                    <tr>
                        <td class="text-left">Elevation</td>
                        <td class="text-left">""" + result['elevation'] + """</td>
                    </tr>
                    <tr>
                        <td class="text-left">Active Minutes</td>
                        <td class="text-left">""" + result['activemins'] + """</td>
                    </tr>
                    <tr>
                        <td class="text-left">Calories</td>
                        <td class="text-left">""" + result['calories'] + """</td>
                    </tr>
                    <tr>
                        <td class="text-left">Pulse</td>
                        <td class="text-left">""" + result['pulse'] + """</td>
                    </tr>
                    <tr>
                        <td class="text-left">Floors</td>
                        <td class="text-left">""" + result['floors'] + """</td>
                    </tr>
                    <tr>
                        <td class="text-left">Steps</td>
                        <td class="text-left">""" + result['steps'] + """</td>
                    </tr>
                    <tr>
                        <td class="text-left">Blood Pressure</td>
                        <td class="text-left">""" + result['bp'] + """</td>
                    </tr>
                </tbody>
            </table>
        </body>
        </html>
		"""


        if(data['duration'] == "dailyall"):
            htmlReportFp.write(htmlResourcesSection)
            htmlReportFp.write(htmlHeadSection)
            htmlReportFp.write(htmlBodySectionForDailyAll)

        #htmlReportFp.write(htmlChartSection)
        #htmlReportFp.write(htmlBodySectionForCharts)

		# print results to shell
        print "Created html report"
        htmlReportFp.close()

        webbrowser.get().open(htmlReportPath)

    except:
		comment = ('EXCEPTION: ' + str(sys.exc_info()[1]))
		print comment
		return 0

#--------------------------------MAIN-------------------------------------------

