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
    del result['Message']
    del result['StatusCode']
    if (len(result) > 0):
        temp = result.keys()
        keys = []
        for i in temp:
            keys.append(int(i))
        keys.sort()
        print keys

    #Create the HTML file for output
    htmlReportPath = os.path.dirname(os.path.realpath(__file__))
    htmlReportPath = os.path.join(htmlReportPath,"report.html")
    htmlReportFp = open(htmlReportPath,"w")
    print htmlReportPath

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

        htmlHeadSection = """
        <head>
			<title>Report</title>
		</head>
        """

        if(data['duration'] == "dailyall"):
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
            htmlReportFp.write(htmlResourcesSection)
            htmlReportFp.write(htmlHeadSection)
            htmlReportFp.write(htmlBodySectionForDailyAll)

        elif(data['duration'] == "daily"):
            htmlChartSection = """
            <!-- Chart code -->
            <script>
            var chart = AmCharts.makeChart("chartdiv", {
                "theme": "none",
                "type": "serial",
            	"startDuration": 2,
                "dataProvider": [ """

            colorsIndex = 0
            colors = ["#FF0F00","#FF6600","#FF9E01","#FCD202","#F8FF01","#B0DE09","#04D215","#92f3aa","#4debc4","#0D8ECF","#36b3f2","#36e2f2","#0D52D1","#2A0CD0","#8A0CCF","#CD0D74","#754DEB","#8764ee","#997bf0","#aa92f3","#4dc3eb","#92daf3","#DDDDDD","#999999","#333333","#000000"]
            for i in keys:
                s = """{
                    "country": """ + str(i) + """,
                    "visits": """ + str(result[str(i)]) + """,
                    "color": " """ + colors[colorsIndex] + """ ",
                },"""
                colorsIndex += 1
                htmlChartSection = htmlChartSection + s

            htmlChartSection = htmlChartSection + """
                 ],

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

            htmlBodySectionForCharts = """
    		<body class="main">
    		<header>
    			<h1 class="heading">Report: """ + reportName + """</h1>
    		</header>
    		<div id="chartdiv"></div>
            </body>
            </html>
    		"""

            htmlReportFp.write(htmlResourcesSection)
            htmlReportFp.write(htmlChartSection)
            htmlReportFp.write(htmlHeadSection)
            htmlReportFp.write(htmlBodySectionForCharts)

		# print results to shell
        print "Created html report"
        htmlReportFp.close()

        webbrowser.get().open(htmlReportPath)

    except:
		comment = ('EXCEPTION: ' + str(sys.exc_info()[1]))
		print comment
		return 0

#--------------------------------MAIN-------------------------------------------

