#-------------------------------------------------------------------------------
# Name:        clientAppRestServer
# Purpose:     This script will act as a REST server for test purposes
#
# Author:      Chaitra Ramachandra
#
# Created:     22/04/2017
# Copyright:   (c) chaitra 2017
#-------------------------------------------------------------------------------

from flask import Flask, jsonify, request
import json

app = Flask(__name__)


@app.route('/post', methods=['GET', 'POST'])
def mypost():
    try:
        if(request.method == 'POST'):
            print "Request: " + str(request)

            if(str(request.json.get('duration'))=="dailyall"):
                response = {"Message": "Per day summary","StatusCode": 200, 'distance': '3.4', 'elevation': '2.1', 'activemins': '23.0', 'calories': '14131.0', 'pulse': '98', 'floors': '1.3', 'steps': '123456', 'date': '2017-04-03', 'bp': '123/78', 'id': '2222222222'}

            elif(str(request.json.get('duration'))=="daily"):
                response = {"Message": "Hourly data retrieved", "0": "0.0","1": "11.0","2": "70.0","3": "141.0", "4": "413.0", "5": "213.0","6": "513.0","7": "113.0","8": "333.0","9": "141.0","10": "181.0","11": "241.0","12": "0.0","13": "13.0","14": "70.0","15": "141.0", "16": "413.0", "17": "213.0","18": "513.0","19": "113.0","20": "333.0","21": "141.0","22": "181.0","23": "241.0","StatusCode": "200"}

            elif(str(request.json.get('duration'))=="weekly"):
                response =  {"Message": "Per week data retrieved", "2017-03-31": 1432.0,"2017-04-01": 10000.0,"2017-04-02": 14132.0, "2017-04-03": 13131.0, "2017-04-04": 15132.0,"2017-04-05": 17132.0,"2017-04-06": 15342.0,"StatusCode": 200}

            elif(str(request.json.get('duration'))=="yearly"):
                response = {"Message": "Yearly data retrieved","January_2017": "98.0","April_2017": "45.0", "February_2017": "67.0","March_2017": "89.0","December_2016": "144.0","November_2016": "70.0", "StatusCode": "200"}

            elif(str(request.json.get('duration'))=="localAreaSummary"):
                response = {"Message": "Local summary data retrieved", "client_summary": {"distance": 3.4, "elevation": 2.1, "activemins": 23.0, "calories": 151.0, "pulse": "98", "floors": 1.3, "steps": 126, "date": "2017-04-03", "bp": 2, "id": "2222222222"}, "localAreaSummary": {"distance": 3.4, "elevation": 2.1, "activemins": 23.0, "ip": "0.0.0.0", "calories": 143.0, "pulse": 98, "floors": 1.3, "steps": 123, "date": "2017-04-03", "bp": "1.576923076"}, "StatusCode": 200}

            else:
                response =  {"Message": "No data retrieved", "StatusCode": 200}
            response = json.dumps(response)
            return response

    except Exception as e:
        return jsonify({'error': str(e)})



if __name__ == '__main__':
    app.run(debug=True)