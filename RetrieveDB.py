def dailyAll(req, db):
    clientId = req["clientId"]
    date = req["date"]
    cursor = db.cursor()
    #select * from hourlysummary where id=2222222222 AND DATE(dateTime)="2017-04-03";
    command = "select * from dailysummary WHERE id=\"" + clientId + "\" AND DATE=\"" + date + "\";"
    print "command = " + str(command) + "\n"
    cursor.execute(command)
    ret = cursor.fetchone()
    '''
    for key in row:
        print type(row)
        print row
        row = cursor.fetchone()
    '''
    if ret is not None:
    	ret["date"] = ret["date"].__str__()
    if ret == None:
	ret = {}
    return ret
    
def daily(req, db):
    clientId = req["clientId"]
    date = req["date"]
    item = req["type"]
    cursor = db.cursor()
    command = "select " + item + " , HOUR(dateTime)  from hourlysummary WHERE id=\"" + clientId + "\" AND DATE(dateTime)=\"" + date + "\";"
    #print "\ncommand = " + str(command) + "\n"
    cursor.execute(command)
    ret = {}
    row = cursor.fetchone()
    while row is not None:
        ret[ row["HOUR(dateTime)"].__str__() ] = row[item]
        row = cursor.fetchone()
    if ret == None:
	ret = {}
    return ret

def weekly(req, db):
    clientId = req["clientId"]
    date = req["date"]
    item = req["type"]
    cursor = db.cursor()
    #select distinct calories, Date from dailysummary  WHERE Date BETWEEN "2017-04-03"-7 AND "2017-04-03" order by Date ASC;
    command = "select distinct " + item + ", DATE from dailysummary WHERE DATE BETWEEN \"" + date + "\"-7 AND \"" + date + "\" AND id = \"" + clientId + "\" order by DATE ASC;"
    #print "\ncommand = " + str(command) + "\n"
    cursor.execute(command)
    ret = {}
    row = cursor.fetchone()
    while row is not None:
        ret[ row["DATE"].__str__() ] = row[item]
        row = cursor.fetchone()
    if ret == None:
	ret = {}
    return ret
    
def monthly(req, db):
    return 1

def yearly(req, db):
    clientId = req["clientId"]
    date = req["date"]
    item = req["type"]
    cursor = db.cursor()
    operation = "SUM"
    if item == "pulse":
        operation = "AVG"
    #select distinct calories, Date from dailysummary  WHERE Date BETWEEN "2017-04-03"-7 AND "2017-04-03" order by Date ASC;
    command = "SELECT " + operation + "("+ item + "),  MONTHNAME(date) , YEAR(date)  FROM dailysummary WHERE id=\"" + clientId + "\" AND date between  \"" + date + "\" - 365 AND \"" + date + "\" GROUP BY MONTHNAME(date), YEAR(date);"
    #print "\ncommand = " + str(command) + "\n"
    cursor.execute(command)
    ret = {}
    row = cursor.fetchone()
    #print "\n", str(row.keys()), "\n"
    while row is not None:
        month = row["MONTHNAME(date)"].__str__()
        year = row["YEAR(date)"].__str__()
        month_year = month + "_" + year
        #print month, year, month_year, "\n"
        ret[ month_year ] = row[operation + "(" + item + ")"]
        row = cursor.fetchone()
    if ret == None:
	ret = {}
    return ret

def localAreaSummary(req, db):
    clientId = req["clientId"]
    date = req["date"]
    ip = req["ip"]
    cursor = db.cursor()
    command = "select * from dailysummary WHERE id=\"" + clientId + "\" AND DATE=\"" + date + "\";"
    cursor.execute(command)
    client_summary = cursor.fetchone()
    if client_summary is not None:
        client_summary["date"] = client_summary["date"].__str__()
    
    command = "select * from localsummary WHERE ip=\"" + ip + "\" AND DATE=\"" + date + "\";"
    #print "\ncommand = " + str(command) + "\n"
    cursor.execute(command)
    localAreaSummary = cursor.fetchone()
    if localAreaSummary is not None:
        localAreaSummary["date"] = localAreaSummary["date"].__str__()
    ret = {}
    ret["localAreaSummary"] = localAreaSummary
    ret["client_summary"] = client_summary
    if ret == None:
	ret = {}
    return ret
