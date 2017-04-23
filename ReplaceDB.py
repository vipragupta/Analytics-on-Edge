def handleHourly(req, db):
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
        cursor.execute(command)
        db.commit()
        
def clientSummary(req, db):
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

def localSummary(req, db):
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
