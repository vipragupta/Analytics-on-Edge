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
#from flaskext.mysql import MySQL
import json

app = Flask(__name__)


@app.route('/post', methods=['GET', 'POST'])
def mypost():
    print "I am here"
    try:
        print "I am here again"
        if(request.method == 'POST'):
            print "Request: " + str(request)
            print request.json

            response = {"Message": "Hourly data retrieved", "0": "0.0","1": "11.0","2": "70.0","3": "141.0", "4": "413.0", "5": "213.0","6": "513.0","7": "113.0","8": "333.0","9": "141.0","10": "181.0","11": "241.0","12": "0.0","13": "13.0","14": "70.0","15": "141.0", "16": "413.0", "17": "213.0","18": "513.0","19": "113.0","20": "333.0","21": "141.0","22": "181.0","23": "241.0","StatusCode": "200"}
            #response =  {"Message": "Daily data retrieved", "2017-04-02": 14132.0, "2017-04-03": 14131.0, "StatusCode": 200}
            #response = {u'distance': '3.4', u'elevation': '2.1', u'activemins': '23.0', u'calories': '14131.0', u'pulse': u'98', u'floors': '1.3', u'steps': '123456', u'date': '2017-04-03', u'bp': '123/78', u'id': u'2222222222'}
            response = json.dumps(response)
            return response

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)