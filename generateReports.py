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

        #Create the HTML file for output
        htmlReportPath = os.path.dirname(os.path.realpath(__file__))
        htmlReportPath = os.path.join(htmlReportPath,"report.html")
        htmlReportFp = open(htmlReportPath,"w")

        #Write html document - COMMON HTML SECTIONS
        htmlResourcesSection, htmlHeadSection = htmlResources()

        if(len(result) > 2):
            del result['Message']
            del result['StatusCode']

            if(data['duration'] == "dailyall"):
                reportName = "Summary for today: " + data['date']
                htmlBodySectionForDailyAll = htmlBodyForDailyAll(reportName, result)
                htmlReportFp.write(htmlResourcesSection)
                htmlReportFp.write(htmlHeadSection)
                htmlReportFp.write(htmlBodySectionForDailyAll)

            elif(data['duration'] == "daily"):
                if (len(result) > 0):
                    temp = result.keys()
                    keys = []
                    for i in temp:
                        keys.append(int(i))
                    keys.sort()
                reportName = "Hourly statistics of " + data['type'].upper() + " for " + data['date']

                htmlChartSection = htmlChartHourly(keys, result)
                htmlBodySectionForCharts = htmlBodyChart(reportName)
                htmlReportFp.write(htmlResourcesSection)
                htmlReportFp.write(htmlChartSection)
                htmlReportFp.write(htmlHeadSection)
                htmlReportFp.write(htmlBodySectionForCharts)

            elif(data['duration'] == "weekly"):
                if(len(result) > 0):
                    temp = result.keys()
                    keys = []
                    for i in temp:
                        keys.append(str(i))
                    keys.sort()
                weekday = {}
                for each_date in keys:
                    datee = dparser.parse(each_date,fuzzy=True)
                    day = calendar.day_name[datee.date().weekday()]
                    weekday[each_date] = day
                reportName = "Statistics of " + data['type'].upper() + " for the duration:  " + str(keys[0]) + "  to  " + str(keys[len(keys)-1])

                htmlChartSection = htmlChartWeekly(keys,weekday,result)
                htmlBodySectionForCharts = htmlBodyChart(reportName)
                htmlReportFp.write(htmlResourcesSection)
                htmlReportFp.write(htmlChartSection)
                htmlReportFp.write(htmlHeadSection)
                htmlReportFp.write(htmlBodySectionForCharts)


            elif(data['duration'] == "yearly"):
                if (len(result) > 0):
                    temp = result.keys()
                    keys = []
                    for i in temp:
                        keys.append(str(i))
                year = data['date'].split('-')[0]
                reportName = "Statistics of " + data['type'].upper() + " for the duration: " + str(int(year)-1) + " - " + str(year)

                htmlChartSection = htmlChartYearly(keys,result)
                htmlBodySectionForCharts = htmlBodyYearly(reportName)
                htmlReportFp.write(htmlResourcesSection)
                htmlReportFp.write(htmlChartSection)
                htmlReportFp.write(htmlHeadSection)
                htmlReportFp.write(htmlBodySectionForCharts)

            elif(data['duration'] == 'localAreaSummary'):
                reportName = "Comparison of your performace with other Fitbit users in your area. Date: " + data['date']
                htmlChartSection = htmlChartLocalArea(result)
                htmlBodySectionForCharts = htmlBodyChart(reportName)
                htmlReportFp.write(htmlResourcesSection)
                htmlReportFp.write(htmlChartSection)
                htmlReportFp.write(htmlHeadSection)
                htmlReportFp.write(htmlBodySectionForCharts)

        else:
            print "No data found for the given duration!"
            htmlDataNotFound = htmlEmpty()
            htmlReportFp.write(htmlDataNotFound)

        print "Created html report"
        htmlReportFp.close()
        webbrowser.get().open(htmlReportPath)

    except:
		comment = ('EXCEPTION: ' + str(sys.exc_info()[1]))
		print comment
		return 0













#----------------------------WRITE HTML COMMON FUNCTIONS------------------------
def htmlResources():
    a = """
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
    b = """
        <head>
			<title>Report</title>
		</head>
        """
    return(a,b)




#----------------------HTML BODY FOR DAILY ALL-----------------------------------
def htmlBodyForDailyAll(reportName, result):
    a = """
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
    return(a)




#-----------------------------HTML CHART HOURLY---------------------------------
def htmlChartHourly(keys, result):
    a = """
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
            "Activity": " """ + str(i) + """ ",
            "Count": """ + str(result[str(i)]) + """,
            "color": " """ + colors[colorsIndex] + """ ",
        },"""
        colorsIndex += 1
        a = a + s

    a = a + """],

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
            "valueField": "Count"
        }],
        "depth3D": 20,
    	"angle": 30,
        "chartCursor": {
            "categoryBalloonEnabled": false,
            "cursorAlpha": 0,
            "zoomable": false
        },
        "categoryField": "Activity",
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
    return(a)

def htmlBodyChart(reportName):
    a = """
		<body class="main">
		<header>
			<h1 class="heading">""" + reportName + """</h1>
		</header>
		<div id="chartdiv"></div>
        </body>
        </html>
		"""
    return(a)


#--------------------------------HTML CHART WEEKLY------------------------------
def htmlChartWeekly(keys,weekday,result):
    a = """
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
            "Day": " """ + str(i) + """ (""" + weekday[i] + """)",
            "Count": """ + str(result[str(i)]) + """,
            "color": " """ + colors[colorsIndex] + """ ",
        },"""
        colorsIndex += 1
        a = a + s

    a = a + """],

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
            "valueField": "Count"
        }],
        "depth3D": 20,
    	"angle": 30,
        "chartCursor": {
            "categoryBalloonEnabled": false,
            "cursorAlpha": 0,
            "zoomable": false
        },
        "categoryField": "Day",
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
    return(a)



#----------------------------HTML CHART YEARLY----------------------------------
def htmlChartYearly(keys,result):
    a = """
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
            "Month": " """ + str(i) + """ ",
            "Summary": " """ + str(result[str(i)]) + """ ",
        },"""
        a = a + s

    a = a + """],
          "valueField": "Summary",
          "titleField": "Month",
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
    return(a)


def htmlBodyYearly(reportName):
    a = """
		<body class="main">
		<header>
			<h1 class="heading">""" + reportName + """</h1>
		</header>
		<div id="chartdiv2"></div>
        </body>
        </html>
		"""
    return(a)


#------------------------------HTML CHART LOCAL AREA----------------------------
def htmlChartLocalArea(result):
    a = """
    <!-- Chart code -->
    <script>
    var chart = AmCharts.makeChart("chartdiv", {
        "theme": "light",
        "type": "serial",
        "dataProvider": [{
            "Activities": "Distance Covered",
            "LocalAreaSummary": """ + str(result['localAreaSummary'].get('distance')) + """,
            "ClientSummary": """ + str(result['client_summary'].get('distance')) + """
        }, {
            "Activities": "Elevation",
            "LocalAreaSummary": """ + str(result['localAreaSummary'].get('elevation')) + """,
            "ClientSummary": """ + str(result['client_summary'].get('elevation')) + """
        }, {
            "Activities": "Active Minutes",
            "LocalAreaSummary": """ + str(result['localAreaSummary'].get('activemins')) + """,
            "ClientSummary": """ + str(result['client_summary'].get('activemins')) + """
        }, {
            "Activities": "Calories Burned",
            "LocalAreaSummary": """ + str(result['localAreaSummary'].get('calories')) + """,
            "ClientSummary": """ + str(result['client_summary'].get('calories')) + """
        }, {
            "Activities": "Steps",
            "LocalAreaSummary": """ + str(result['localAreaSummary'].get('steps')) + """,
            "ClientSummary": """ + str(result['client_summary'].get('steps')) + """
        }, {
            "Activities": "Number of floors",
            "LocalAreaSummary": """ + str(result['localAreaSummary'].get('floors')) + """,
            "ClientSummary": """ + str(result['client_summary'].get('floors')) + """
        }, {
            "Activities": "Pulse",
            "LocalAreaSummary": """ + str(result['localAreaSummary'].get('pulse')) + """,
            "ClientSummary": """ + str(result['client_summary'].get('pulse')) + """
        }, {
            "Activities": "Blood Pressure",
            "LocalAreaSummary": """ + str(result['localAreaSummary'].get('bp')) + """,
            "ClientSummary": """ + str(result['client_summary'].get('bp')) + """
        }],
        "valueAxes": [{
            "position": "left",
            "title": "Count",
        }],
        "startDuration": 1,
        "graphs": [{
            "balloonText": "Area Summary - [[category]]: <b>[[value]]</b>",
            "fillAlphas": 0.9,
            "lineAlpha": 0.2,
            "title": "LocalAreaSummary",
            "type": "column",
            "valueField": "LocalAreaSummary"
        }, {
            "balloonText": "My Summary - [[category]]: <b>[[value]]</b>",
            "fillAlphas": 0.9,
            "lineAlpha": 0.2,
            "title": "ClientSummary",
            "type": "column",
            "clustered":false,
            "columnWidth":0.5,
            "valueField": "ClientSummary"
        }],
        "plotAreaFillAlphas": 0.1,
        "categoryField": "Activities",
        "categoryAxis": {
            "gridPosition": "start"
        },
        "export": {
        	"enabled": true
         }

    });
    </script>
    """
    return(a)



#-------------------------------DATA NOT FOUND----------------------------------
def htmlEmpty():
    a = """
		<!DOCTYPE html>
		<html>
            <!-- Resources -->
            <link rel="stylesheet" href="style.css" type="text/css"/>
            <head>
                <title>Report</title>
            </head>
            <body class="main">
    		  <div id="empty"><img src="http://www.mediafire.com/imgbnc.php/ecd61d89ed2f5d16bd376bbc31d0701d695acd53787484fa6cdd7ce3f27be5df6g.jpg" alt="Data not found for that day/period"></div>
            </body>
        </html>
        """
    return(a)


#--------------------------------MAIN-------------------------------------------

