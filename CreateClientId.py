from random import randint

list = []
for i in range(0,100):
	id = str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9))+ str(randint(0,9))+ str(randint(0,9)) + str(randint(0,9))+ str(randint(0,9))+ str(randint(0,9))
	list.append(id)

fileW = open("clientIds.txt", 'w')

for item in list:
	fileW.write("%s\n" % item)

fileW.close()