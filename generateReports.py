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
    print result
    try:
        if(data['duration'] == "dailyall"):
            reportName = "Summary for " + data['date']
            bpList = (result['bp']).split("/")
        elif(data['duration'] == "daily"):
            reportName = "Hourly statistics of " + data['type'] + " for " + data['date']
		# Create the HTML file for output
        htmlReportPath = os.path.dirname(os.path.realpath(__file__))
        htmlReportPath = os.path.join(htmlReportPath,"report.html")
        htmlReportFp = open(htmlReportPath,"w")
        #print htmlReportPath

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

                    "country": "Blood Pressure Systolic",
                    "visits": """ + bpList[0] + """,
                    "color": "#B0DE09"
                }, {

                    "country": "Blood Pressure Diastolic",
                    "visits": """ + bpList[1] + """,
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

#--------------------------------MAIN-------------------------------------------

