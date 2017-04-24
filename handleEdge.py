from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
import datetime
from ReplaceDB import handleHourly, clientSummary, localSummary
from RetrieveDB import dailyAll, daily, weekly, monthly, yearly, localAreaSummary
from pymysql.cursors import DictCursor
import json 

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Abcd@1234'
app.config['MYSQL_DATABASE_DB'] = 'analytics'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL(app, cursorclass=DictCursor)
db = mysql.connect()

@app.route('/pushdata', methods=['GET', 'POST'])
def pushdata():#from edge server
    req = request.json
    req = {'hourly': {'1234567890': {'distance': '3.4', 'floors': '1.3', 'steps': '123456', 'calories': '14131', 'hour': '3', 'date': '2017-04-03', 'elevation': '2.1', 'bp': '123/78', 'active': '23', 'pulse': '98'}, '2222222222': {'distance': '3.4', 'floors': '1.3', 'steps': '123456', 'calories': '14131', 'hour': '3', 'date': '2017-04-03', 'elevation': '2.1', 'bp': '123/78', 'active': '23', 'pulse': '98'}}, 'localSummary': {'elevation': '2.1', 'distance': '3.4', 'floors': '1.3', 'steps': '123456', 'calories': '14131', 'date': '2017-04-03', 'ip': '0.0.0.0', 'bp': '123/78', 'active': '23', 'pulse': '98'}, 'clientSummary': {'1234567890': {'distance': '3.4', 'floors': '1.3', 'steps': '123456', 'calories': '14131', 'date': '2017-04-03', 'elevation': '2.1', 'bp': '123/78', 'active': '23', 'pulse': '98'}, '2222222222': {'distance': '3.4', 'floors': '1.3', 'steps': '123456', 'calories': '14131', 'date': '2017-04-03', 'elevation': '2.1', 'bp': '123/78', 'active': '23', 'pulse': '98'}}}
    
    if( "hourly" in req ):
        handleHourly(req["hourly"], db)
    if( "clientSummary" in req):
        clientSummary(req["clientSummary"], db)
    if( "localSummary" in req ):
        localSummary(req["localSummary"], db)
    return jsonify({'StatusCode':'200','Message': 'Database addition/replacement success'})

@app.route('/getreport', methods=['GET', 'POST'])
def getreport():#from client
    req = request.json
    req = {	
            "clientId": "2222222222",
            "duration": "localAreaSummary",
            "date": "2017-04-03",
            "type" : "pulse",
            "ip" : "0.0.0.0"
        }
    if "duration" not in req:
        print "duration not in req"
        return jsonify({'StatusCode':'400','Message': 'Invalid request, please provide duration, clientid, time and other details'})
    
    duration = req["duration"]
    print "duration = " + str(duration) + "\n"
    if(duration == "dailyall"):
        ret = dailyAll(req, db)
        ret['StatusCode'] = 200
        ret['Message'] = 'Summary data retrieved'
        return json.dumps(ret)
    elif(duration == "daily"):
        ret = daily(req, db)
        ret['StatusCode'] = 200
        ret['Message'] = 'Hourwise data retrieved'
        return json.dumps(ret)
    elif(duration == "weekly"):
        ret = weekly(req, db)
        print ret
        ret['StatusCode'] = 200
        ret['Message'] = 'Daywise data retrieved'
        return json.dumps(ret)
    elif(duration == "yearly"):
        ret = yearly(req, db)
        print ret
        ret['StatusCode'] = 200
        ret['Message'] = 'Monthwise data retrieved'
        return json.dumps(ret)
    elif(duration == "localAreaSummary"):
        ret = localAreaSummary(req, db)
        print ret
        ret['StatusCode'] = 200
        ret['Message'] = 'Local summary data retrieved'
        return json.dumps(ret)
    '''
    elif(duration == "monthly"):
        #do something
    '''
    return jsonify({'StatusCode':'200','Message': 'Database search result'})

if __name__ == '__main__':
    app.run(debug=True)
