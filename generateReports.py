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
import dateutil.parser as dparser
import calendar

colors = ["#FF0F00","#FF6600","#FF9E01","#FCD202","#F8FF01","#B0DE09","#04D215","#92f3aa","#4debc4","#0D8ECF","#36b3f2","#36e2f2","#0D52D1","#2A0CD0","#8A0CCF","#CD0D74","#754DEB","#8764ee","#997bf0","#aa92f3","#4dc3eb","#92daf3","#DDDDDD","#999999","#333333","#000000"]

#-------------------Generate Graph and create HTML Report-----------------------
def displayGraph(data,result):
    try:
        global html
        print "RESULT in displayGraph():", result

        #Create the HTML file for output
        htmlReportPath = os.path.dirname(os.path.realpath(__file__))
        htmlReportPath = os.path.join(htmlReportPath,"report.html")
        htmlReportFp = open(htmlReportPath,"w")
    ##    print htmlReportPath
    ##    print "********************"

        if(len(result) > 2):
            del result['Message']
            del result['StatusCode']

            if(data['duration'] == "dailyall"):
                reportName = "Summary for today: " + data['date']
    ##                bpList = (result['bp']).split("/")

            elif(data['duration'] == "daily"):
                if (len(result) > 0):
                    temp = result.keys()
                    keys = []
                    for i in temp:
                        keys.append(int(i))
                    keys.sort()
    ##                    print keys
                reportName = "Hourly statistics of " + data['type'].upper() + " for " + data['date']

            elif(data['duration'] == "weekly"):
                if(len(result) > 0):
                    temp = result.keys()
                    keys = []
                    for i in temp:
                        keys.append(str(i))
                    keys.sort()
                    print keys

                print "**********************"

                weekday = {}
                for each_date in keys:
                    datee = dparser.parse(each_date,fuzzy=True)
                    day = calendar.day_name[datee.date().weekday()]
                    weekday[each_date] = day

                print weekday
                reportName = "Statistics of " + data['type'].upper() + " for the duration:  " + str(keys[0]) + "  to  " + str(keys[len(keys)-1])


            elif(data['duration'] == "yearly"):
                if (len(result) > 0):
                    temp = result.keys()
                    keys = []
                    for i in temp:
                        keys.append(str(i))
                year = data['date'].split('-')[0]
                reportName = "Statistics of " + data['type'].upper() + " for the duration: " + str(int(year)-1) + " - " + str(year)

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
                <script src="https://www.amcharts.com/lib/3/pie.js"></script>
                <script src="https://www.amcharts.com/lib/3/themes/light.js"></script>
                <link rel="stylesheet" href="style.css" type="text/css"/>
            """

            htmlHeadSection = """
            <head>
    			<title>Report</title>
    		</head>
            """

            #Graph for per day statistics for all items
            if(data['duration'] == "dailyall"):
                htmlBodySectionForDailyAll = """
                    <body>
                        <header>
                            <h1 class="heading">""" + reportName + """</h1>
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
                                    <td class="text-left">""" + str(result['distance']) + """</td>
                                </tr>
                                <tr>
                                    <td class="text-left">Elevation</td>
                                    <td class="text-left">""" + str(result['elevation']) + """</td>
                                </tr>
                                <tr>
                                    <td class="text-left">Active Minutes</td>
                                    <td class="text-left">""" + str(result['activemins']) + """</td>
                                </tr>
                                <tr>
                                    <td class="text-left">Calories</td>
                                    <td class="text-left">""" + str(result['calories']) + """</td>
                                </tr>
                                <tr>
                                    <td class="text-left">Pulse</td>
                                    <td class="text-left">""" + str(result['pulse']) + """</td>
                                </tr>
                                <tr>
                                    <td class="text-left">Floors</td>
                                    <td class="text-left">""" + str(result['floors']) + """</td>
                                </tr>
                                <tr>
                                    <td class="text-left">Steps</td>
                                    <td class="text-left">""" + str(result['steps']) + """</td>
                                </tr>
                                <tr>
                                    <td class="text-left">Blood Pressure</td>
                                    <td class="text-left">""" + str(result['bp']) + """</td>
                                </tr>
                            </tbody>
                        </table>
                    </body>
                    </html>
            		"""
                htmlReportFp.write(htmlResourcesSection)
                htmlReportFp.write(htmlHeadSection)
                htmlReportFp.write(htmlBodySectionForDailyAll)

            #Graph for hourly statistics for one item Eg: Calories
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

                for i in keys:
                    s = """{
                        "country": " """ + str(i) + """ ",
                        "visits": """ + str(result[str(i)]) + """,
                        "color": " """ + colors[colorsIndex] + """ ",
                    },"""
                    colorsIndex += 1
                    htmlChartSection = htmlChartSection + s

                htmlChartSection = htmlChartSection + """
                     ],

                    "valueAxes": [{
                        "position": "left",
                        "title": "Count",
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
                        "labelRotation": 0
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
        			<h1 class="heading">""" + reportName + """</h1>
        		</header>
        		<div id="chartdiv"></div>
                </body>
                </html>
        		"""

                htmlReportFp.write(htmlResourcesSection)
                htmlReportFp.write(htmlChartSection)
                htmlReportFp.write(htmlHeadSection)
                htmlReportFp.write(htmlBodySectionForCharts)


            #Graph for one week statistics for one item Eg: Calories
            elif(data['duration'] == "weekly"):
                htmlChartSection = """
                <!-- Chart code -->
                <script>
                    var chart = AmCharts.makeChart("chartdiv", {
                    "theme": "none",
                    "type": "serial",
                	"startDuration": 2,
                    "dataProvider": [ """

                colorsIndex = 0

                for i in keys:
                    s = """{
                        "country": " """ + str(i) + """ (""" + weekday[i] + """)",
                        "visits": """ + str(result[str(i)]) + """,
                        "color": " """ + colors[colorsIndex] + """ ",
                    },"""
                    colorsIndex += 1
                    htmlChartSection = htmlChartSection + s

                htmlChartSection = htmlChartSection + """
                     ],

                    "valueAxes": [{
                        "position": "left",
                        "title": "Count",
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
                        "labelRotation": 0
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
        			<h1 class="heading">""" + reportName + """</h1>
        		</header>
        		<div id="chartdiv"></div>
                </body>
                </html>
        		"""

                htmlReportFp.write(htmlResourcesSection)
                htmlReportFp.write(htmlChartSection)
                htmlReportFp.write(htmlHeadSection)
                htmlReportFp.write(htmlBodySectionForCharts)


            #Graph for per year statistics of one item
            elif(data['duration'] == "yearly"):
                htmlChartSection = """
                    <!-- Chart code -->
                    <script>
                    var chart = AmCharts.makeChart("chartdiv2", {
                      "type": "pie",
                      "startDuration": 0,
                       "theme": "light",
                      "addClassNames": true,
                      "legend":{
                       	"position":"right",
                        "marginRight":100,
                        "autoMargins":false
                      },
                      "innerRadius": "30%",
                      "defs": {
                        "filter": [{
                          "id": "shadow",
                          "width": "200%",
                          "height": "200%",
                          "feOffset": {
                            "result": "offOut",
                            "in": "SourceAlpha",
                            "dx": 0,
                            "dy": 0
                          },
                          "feGaussianBlur": {
                            "result": "blurOut",
                            "in": "offOut",
                            "stdDeviation": 5
                          },
                          "feBlend": {
                            "in": "SourceGraphic",
                            "in2": "blurOut",
                            "mode": "normal"
                          }
                        }]
                      },
                      "dataProvider": [ """

                for i in keys:
                    s = """{
                        "country": " """ + str(i) + """ ",
                        "litres": " """ + str(result[str(i)]) + """ ",
                    },"""
                    htmlChartSection = htmlChartSection + s

                htmlChartSection = htmlChartSection + """
                     ],
                      "valueField": "litres",
                      "titleField": "country",
                      "export": {
                        "enabled": true
                      }
                    });

                    chart.addListener("init", handleInit);

                    chart.addListener("rollOverSlice", function(e) {
                      handleRollOver(e);
                    });

                    function handleInit(){
                      chart.legend.addListener("rollOverItem", handleRollOver);
                    }

                    function handleRollOver(e){
                      var wedge = e.dataItem.wedge.node;
                      wedge.parentNode.appendChild(wedge);
                    }
                    </script>
                    """

                htmlBodySectionForCharts = """
        		<body class="main">
        		<header>
        			<h1 class="heading">""" + reportName + """</h1>
        		</header>
        		<div id="chartdiv2"></div>
                </body>
                </html>
        		"""

                htmlReportFp.write(htmlResourcesSection)
                htmlReportFp.write(htmlChartSection)
                htmlReportFp.write(htmlHeadSection)
                htmlReportFp.write(htmlBodySectionForCharts)

            elif(data['duration'] == "localAreaSummary"):
                print "*****************************"

    		# print results to shell
            print "Created html report"
            htmlReportFp.close()

            webbrowser.get().open(htmlReportPath)

        else:
            print "No data found for the given duration!"
            htmlResourcesSection = """
    		<!DOCTYPE html>
    		<html>
                <!-- Resources -->
                <link rel="stylesheet" href="style.css" type="text/css"/>
                <head>
                    <title>Report</title>
                </head>
            """
            htmlReportFp.write(htmlResourcesSection)
            htmlEmpty = """
                <body class="main">
        		<div id="empty"><img src="http://www.mediafire.com/imgbnc.php/ecd61d89ed2f5d16bd376bbc31d0701d695acd53787484fa6cdd7ce3f27be5df6g.jpg" alt="Data not found for that day/period"></div>
                </body>
                </html>
            """
            htmlReportFp.write(htmlEmpty)

    		# print results to shell
            print "Created html report"
            htmlReportFp.close()

            webbrowser.get().open(htmlReportPath)

    except:
		comment = ('EXCEPTION: ' + str(sys.exc_info()[1]))
		print comment
		return 0

#--------------------------------MAIN-------------------------------------------

