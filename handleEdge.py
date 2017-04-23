from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
import datetime
from ReplaceDB import handleHourly, clientSummary, localSummary

mysql = MySQL()
app = Flask(__name__)
app2 = Flask("temp")

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Abcd@1234'
app.config['MYSQL_DATABASE_DB'] = 'analytics'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL(app)
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
    return jsonify({'StatusCode':'200','Message': 'User creation success'})


'''
@app.route('/getreport', methods=['GET', 'POST'])
def getreport():#from client
    cursor = db.cursor()
    command = "INSERT INTO hourlydata (id, dateTime, steps, distance, elevation, calories, floors, pulse, activemins, bp) VALUES (\"1\", \""
    command += str(datetime.time())
    command += "\", 10, 1.2, 21.1, 21.1, 1, 13, 312, \"3424\")"
    #print command
    cursor.execute(command)
    vals = cursor.execute(\'''SELECT * from hourlydata\''')
    print vals
    db.commit()
    return jsonify({'StatusCode':'200','Message': 'User creation success'})
'''

if __name__ == '__main__':
    app.run(debug=True)
