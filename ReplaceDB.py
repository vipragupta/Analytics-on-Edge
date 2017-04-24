import ast

def handleHourly(req, db):
    cursor = db.cursor()
    for i in req.keys():
        client = i
        data = req[i]
        if data == None:
	    continue
	print type(data)
	if type(data) == "str" or type(data) == "unicode":
		data = ast.literal_eval(data)
	date = data.get("date")
        hr = data.get("hour")
        if date == None or hr == None:
            continue
        dateTime = date + " " + str(hr) + ":00:00"
        steps = data.get("steps")
        elevation = data.get("elevation")
        distance = data.get("distance")
        floors = data.get("floors")
        bp = data.get("bp")
        pulse = data.get("pulse")
        calories = data.get("calories")
        activemins = data.get("active")
        
        if client == None or date == None or hr == None or steps == None or elevation == None or distance == None or floors == None or bp == None or pulse == None or calories == None or activemins == None:
                continue

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
	if data == None:
		continue
	print type(data)
	if type(data) == "str" or type(data) == "unicode":
		print "********************************************hitting here\n"
		data = ast.literal_eval(data)
	print type(data)
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
        
        if client == None or date == None or steps == None or elevation == None or distance == None or floors == None or bp == None or pulse == None or calories == None or activemins == None:
            continue

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
    print req
    ip = req.get("edge_ip")
    date = req.get("date")
    steps = req.get("steps")
    elevation = req.get("elevation")
    distance = req.get("distance")
    floors = req.get("floors")
    bp = req.get("bp")
    pulse = req.get("pulse")
    calories = req.get("calories")
    activemins = req.get("active")

    if ip == None or date == None or steps == None or elevation == None or distance == None or floors == None or bp == None or pulse == None or calories == None or activemins == None:
        print "something missing"
	return

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
