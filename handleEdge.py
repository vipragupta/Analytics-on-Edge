from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
import datetime
from ReplaceDB import handleHourly, clientSummary, localSummary
from RetrieveDB import dailyAll, daily, weekly, monthly, yearly, localAreaSummary
from pymysql.cursors import DictCursor
import json 
import ast

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
    print type(req)
    print req 
    print "\n#############################\n"
    
    if( "hourly" in req ):
	inter = req["hourly"]
	print inter
	print type(inter)
        handleHourly(inter , db)
    if( "clientSummary" in req):
	inter = req["clientSummary"]
	print inter
	print type(inter)
        clientSummary(inter, db)
    if( "localSummary" in req ):
	inter = req["localSummary"]
	print inter
	print type(inter)
        localSummary(inter, db)
    return jsonify({'StatusCode':'200','Message': 'Database addition/replacement success'})

@app.route('/getreport', methods=['GET', 'POST'])
def getreport():#from client
    req = request.json
    print str(req), type(req), "\n"
 
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

#if __name__ == '__main__':
#    app.run(debug=True)
