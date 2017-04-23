import json

refineData():
	i = 10
	data = {}
	filename = ["calories", "distance", "elevation", "floors", "steps"]
	while i < 31:
		eachData = {}
		for file in filename:
			path = "/home/vipra/Rbitfit/fitcoach/fitcoach/inst/extdata/intra-daily-timeseries/intra-"+file+"-2015-12-" + str(i) + ".json" ;
			with open(path) as json_data:
			    d = json.load(json_data)
			    eachData[file] = d
			   # print(d)
		data[i] = eachData
		i = i+1
	#print data[10]['calories']

	dataMap = {}
	
	for date in data:
		#print data.keys()
		#print data[date].keys()
		
		i = 0
		tempMap = {}
		while i < 5:
			listC = []
		#	print data[date][filename[i]].keys()
			s = 'activities-'+filename[i] + "-intraday"
			list = data[date][filename[i]][s]['dataset']
		
			for map in list :
				listC.append(map['value'])
		#	print len(listC)

			tempMap[filename[i]] = listC
			
		#	print dataMap.keys()
		#	print
			i+=1
		dataMap[date] = tempMap
	
	finalList = {}
	#print dataMap.keys()
	date = 10
	while date < 31:
		i = 0
		final = []
		while i < 96:
			map = {}
	#		print dataMap[date].keys()
			map["calories"] = dataMap[date]["calories"][i]
			map["distance"] = dataMap[date]['distance'][i]
			map["elevation"] = dataMap[date]["elevation"][i]
			map["floors"] = dataMap[date]["floors"][i]
			map["steps"] = dataMap[date]["steps"][i]
			map["bp"] = generateBP()
			map["pulse"] = generatePulse()
			i +=1
			final.append(map)
		finalList[date] = final
		date +=1

	print finalList.keys()
	
	for date in finalList:
		print len(finalList[date])
		
		fileW = open("dataset/" + str(date) + "_dataset.txt", 'w')
		for item in finalList[date]:
  			fileW.write("%s\n" % item)
		fileW.close()

refineData()