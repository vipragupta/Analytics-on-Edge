from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
import datetime

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

def handleHourly(req):
    cursor = db.cursor()
    for i in req.keys():
        client = i
        data = req[i]
        date = data.get("date")
        hr = data.get("hour")
        dateTime = date + " " + str(hr) + ":00:00"
        steps = data.get("steps")
        elevation = data.get("elevation")
        distance = data.get("distance")
        floors = data.get("floors")
        bp = data.get("bp")
        steps = data.get("steps")
        pulse = data.get("pulse")
        calories = data.get("calories")
        activemins = data.get("active")
        
        command = "REPLACE INTO hourlysummary (id, dateTime, steps, distance, elevation, calories, floors, pulse, activemins, bp) VALUES (\"" 
        command += client + "\", \""
        command += str(dateTime) + "\", "
        command += steps + ", "
        command += distance + ", "
        command += elevation + ", "
        command += calories + ", "
        command += floors + ", "
        command += pulse + ", "
        command += activemins + ", "
        command += bp + ")"
        #print command
        #break
        cursor.execute(command)
        db.commit()
        
def clientSummary(req):
    cursor = db.cursor()
    for i in req.keys():
        client = i
        data = req[i]
        date = data.get("date")
        steps = data.get("steps")
        elevation = data.get("elevation")
        distance = data.get("distance")
        floors = data.get("floors")
        bp = data.get("bp")
        steps = data.get("steps")
        pulse = data.get("pulse")
        calories = data.get("calories")
        activemins = data.get("active")
        
        command = "REPLACE INTO dailysummary (id, date, steps, distance, elevation, calories, floors, pulse, activemins, bp) VALUES (\"" 
        command += client + "\", "
        command += "\"" + date + "\", "
        command += steps + ", "
        command += distance + ", "
        command += elevation + ", "
        command += calories + ", "
        command += floors + ", "
        command += pulse + ", "
        command += activemins + ", "
        command += bp + ")"
        cursor.execute(command)
        db.commit()  

def localSummary(req):
    cursor = db.cursor()
    ip = req.get("ip")
    date = req.get("date")
    steps = req.get("steps")
    elevation = req.get("elevation")
    distance = req.get("distance")
    floors = req.get("floors")
    bp = req.get("bp")
    steps = req.get("steps")
    pulse = req.get("pulse")
    calories = req.get("calories")
    activemins = req.get("active")

    command = "REPLACE INTO localsummary (ip, date, steps, distance, elevation, calories, floors, pulse, activemins, bp) VALUES (\"" 
    command +=  ip + "\", "
    command += "\"" + date + "\", "
    command +=  steps + ", "
    command +=  distance + ", "
    command +=  elevation + ", "
    command +=  calories + ", "
    command +=  floors + ", "
    command +=  pulse + ", "
    command +=  activemins + ", "
    command +=  bp + ")"
    cursor.execute(command)
    db.commit()

@app.route('/pushdata', methods=['GET', 'POST'])
def pushdata():#from edge server
    req = {'hourly': {'1234567890': {'distance': '3.4', 'floors': '1.3', 'steps': '123456', 'calories': '14131', 'hour': '3', 'date': '2017-04-03', 'elevation': '2.1', 'bp': '123/78', 'active': '23', 'pulse': '98'}, '2222222222': {'distance': '3.4', 'floors': '1.3', 'steps': '123456', 'calories': '14131', 'hour': '3', 'date': '2017-04-03', 'elevation': '2.1', 'bp': '123/78', 'active': '23', 'pulse': '98'}}, 'localSummary': {'elevation': '2.1', 'distance': '3.4', 'floors': '1.3', 'steps': '123456', 'calories': '14131', 'date': '2017-04-03', 'ip': '0.0.0.0', 'bp': '123/78', 'active': '23', 'pulse': '98'}, 'clientSummary': {'1234567890': {'distance': '3.4', 'floors': '1.3', 'steps': '123456', 'calories': '14131', 'date': '2017-04-03', 'elevation': '2.1', 'bp': '123/78', 'active': '23', 'pulse': '98'}, '2222222222': {'distance': '3.4', 'floors': '1.3', 'steps': '123456', 'calories': '14131', 'date': '2017-04-03', 'elevation': '2.1', 'bp': '123/78', 'active': '23', 'pulse': '98'}}}

    if( "hourly" in req ):
        handleHourly(req["hourly"])
    if( "clientSummary" in req):
        clientSummary(req["clientSummary"])
    if( "localSummary" in req ):
        localSummary(req["localSummary"])
        
    #cursor = db.cursor()
    #command = "INSERT INTO hourlydata (id, dateTime, steps, distance, elevation, calories, floors, pulse, activemins, bp) VALUES (\"1\", \""
    #command += str(datetime.time())
    #command += "\", 10, 1.2, 21.1, 21.1, 1, 13, 312, \"3424\")"
    #print command
    #cursor.execute(command)
    #vals = cursor.execute('''SELECT * from hourlydata''')
    #print vals
    #db.commit()
    return jsonify({'StatusCode':'200','Message': 'User creation success'})

###########################################################################################################
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
