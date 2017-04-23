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
    for i in req.keys():
        client = i
        data = req.get(i)
        date = data.get("date")
        hour = data.get("hour")
        dateTime = date + " " + str(hr) + ":00:00"
        steps = data.get(steps)
        elevation = data.get("elevation")
        distance = data.get("distance")
        floors = data.get("floors")
        bp = data.get("bp")
        steps = data.get("steps")
        pulse = data.get("pulse")
        activemins = data.get("activemins")
        
        command = "INSERT INTO hourlysummary (id, dateTime, steps, distance, elevation, calories, floors, pulse, activemins, bp) VALUES (\"" 
        + client + "\", "
        + dateTime + ", "
        + steps + ", "
        + distance + ", "
        + elevation + ", "
        + calories + ", "
        + floors + ", "
        + pulse + ", "
        + activemins + ", "
        + bp + ")"
        cursor.execute(command)
        db.commit()
        
def clientSummary(req):
    for i in req.keys():
        client = i
        data = req.get(i)
        date = data.get("date")
        hr = data.get("hour")
        dateTime = date + " " + str(hr) + ":00:00"
        steps = data.get(steps)
        elevation = data.get("elevation")
        distance = data.get("distance")
        floors = data.get("floors")
        bp = data.get("bp")
        steps = data.get("steps")
        pulse = data.get("pulse")
        activemins = data.get("activemins")
        
        command = "INSERT INTO dailysummary (id, dateTime, steps, distance, elevation, calories, floors, pulse, activemins, bp) VALUES (\"" 
        + client + "\", "
        + dateTime + ", "
        + steps + ", "
        + distance + ", "
        + elevation + ", "
        + calories + ", "
        + floors + ", "
        + pulse + ", "
        + activemins + ", "
        + bp + ")"
        cursor.execute(command)
        db.commit()  

def localSummary(req):
    ip = req.get(ip)
    data = req.get(i)
    date = data.get("date")
    time = data.get("hour")
    steps = data.get(steps)
    elevation = data.get("elevation")
    distance = data.get("distance")
    floors = data.get("floors")
    bp = data.get("bp")
    steps = data.get("steps")
    pulse = data.get("pulse")
    activemins = data.get("activemins")

    command = "INSERT INTO localsummary (ip, date, steps, distance, elevation, calories, floors, pulse, activemins, bp) VALUES (\"" 
    + ip + "\", "
    + date + ", "
    + steps + ", "
    + distance + ", "
    + elevation + ", "
    + calories + ", "
    + floors + ", "
    + pulse + ", "
    + activemins + ", "
    + bp + ")"
    cursor.execute(command)
    db.commit()

@app.route('/pushdata', methods=['GET', 'POST'])
def pushdata():#from edge server
    req = request.json #get request from edge server
    if( "hourly" in req ):
        handleHourly(req)
    if( "clientSummary" in req):
        clientSummary(req)
    if( "localSummary" in req ):
        localSummary(req)
        
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
