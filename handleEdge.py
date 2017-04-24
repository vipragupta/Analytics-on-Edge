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

#if __name__ == '__main__':
#    app.run(debug=True)
