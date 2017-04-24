def dailyAll(req, db):
    clientId = req["clientId"]
    date = req["date"]
    cursor = db.cursor()
    #select * from hourlysummary where id=2222222222 AND DATE(dateTime)="2017-04-03";
    command = "select * from dailysummary WHERE id=" + clientId + " AND DATE=\"" + date + "\";"
    #print "command = " + str(command) + "\n"
    cursor.execute(command)
    ret = cursor.fetchone()
    '''
    for key in row:
        print type(row)
        print row
        row = cursor.fetchone()
    '''
    ret["date"] = ret["date"].__str__()
    return ret
    
def daily(req, db):
    clientId = req["clientId"]
    date = req["date"]
    item = req["type"]
    cursor = db.cursor()
    command = "select " + item + " , HOUR(dateTime)  from hourlysummary WHERE id=" + clientId + " AND DATE(dateTime)=\"" + date + "\";"
    #print "\ncommand = " + str(command) + "\n"
    cursor.execute(command)
    ret = {}
    row = cursor.fetchone()
    while row is not None:
        ret[ row["HOUR(dateTime)"].__str__() ] = row[item]
        row = cursor.fetchone()
    return ret

def weekly(req, db):
    clientId = req["clientId"]
    date = req["date"]
    item = req["type"]
    cursor = db.cursor()
    #select distinct calories, Date from dailysummary  WHERE Date BETWEEN "2017-04-03"-7 AND "2017-04-03" order by Date ASC;
    command = "select distinct " + item + ", DATE from dailysummary WHERE DATE BETWEEN \"" + date + "\"-7 AND \"" + date + "\" AND id = " + clientId + " order by DATE ASC;"
    #print "\ncommand = " + str(command) + "\n"
    cursor.execute(command)
    ret = {}
    row = cursor.fetchone()
    while row is not None:
        ret[ row["DATE"].__str__() ] = row[item]
        row = cursor.fetchone()
    return ret
    
def monthly(req, db):
    return 1

def yearly(req, db):
    return 1

def localAreaSummary(req, db):
    return 1
