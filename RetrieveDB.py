def dailyAll(req, db):
    duration = "dailyall"
    print "duration = " + str(duration) + "\n"
    clientId = req["clientId"]
    date = req["date"]
    cursor = db.cursor()
    #select * from hourlysummary where id=2222222222 AND DATE(dateTime)="2017-04-03";
    command = "select * from hourlysummary where id=" + clientId + " AND DATE(dateTime)=\"" + date + "\";"
    print "command = " + str(command) + "\n"
    cursor.execute(command)
    row = cursor.fetchone()
    while row is not None:
        print(row)
        row = cursor.fetchone()
    return 1
    
def daily(req, db):
    return 1

def weekly(req, db):
    return 1
    
def monthly(req, db):
    return 1

def yearly(req, db):
    return 1

def localAreaSummary(req, db):
    return 1
