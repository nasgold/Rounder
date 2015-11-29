YEAR = 2015

def main():


	#Things to do:
	#format stats in text file, such that all non-averaged stats come first
	#maybe, let's put a blank stat in for the seperator
	#thin about how these rows should look in the text file...


	# currently, only for atlanta, will need to do it for each team
	rawStats = getRawStatsFromTextFile()

	for numberOfGamesToGetAverageFor in range(2,3):
		calculateGameAverages(numberOfGamesToGetAverageFor, rawStats)


def calculateGameAverages(numberOfGamesToGetAverageFor, rawStats):

	for gameNumber in range(numberOfGamesToGetAverageFor, len(rawStats)):
		currentRow = rawStats[gameNumber]
		pastRowsToGetAverageFor = getPastRowsToAverage(numberOfGamesToGetAverageFor, rawStats, gameNumber)

		averagedPastStats = averagePastRows(pastRowsToGetAverageFor)


		#safeAveragedStats


def averagePastRows(pastRowsToGetAverageFor):

	statIndexesNotToAverage = getIndexesNotToGetTheAverageFor()
	
	# summedPastStats is a dictionary of the following form...
	# key: stat index.
	# value: the value of each stat (with that index) for each row in pastRowsToGetAverageFor
	summedPastStats = {}
	for row in pastRowsToGetAverageFor:
		row = row.split(',')
		for index in range(len(row)):
			if index not in statIndexesNotToAverage:
				try:
					oldValue = summedPastStats[str(index)]
					summedPastStats[str(index)] = float(row[index]) + float(oldValue)
				except:
					summedPastStats[str(index)] = float(row[index])


	numberOfRows = len(pastRowsToGetAverageFor)
	averageStats = averageSummedPastLists(numberOfRows, summedPastStats)

	return averageStats

def averageSummedPastLists(numberOfRows, summedPastStats):

	keyList = []
	for key in summedPastStats:
		keyList.append(int(key))

	keyList.sort()
	
	averageStats = []
	for key in keyList:
		averageStats.append(summedPastStats[str(key)])

	return averageStats


def getIndexesNotToGetTheAverageFor():

	# Not averaging index 0: gameNumber
	# Not averaging index 1: date of the game
	# Not averaging index 2: home or away
	# Not averaging index 3: opponent
	# Not averaging index 4: result of the game
	# Not averaging index 33: the spread result
	# Not averaging index 34: the spread
	# Not averaging index 35: over under result
	# Not averaging index 36: over under line
	# Not averaging index 37: was this game a back to back?

	return [0, 1, 2, 3, 4, 33, 34, 35, 36, 37]


def getPastRowsToAverage(numberOfGamesToGetAverageFor, rawStats, gameNumber):
	pastRowsToGetAverageFor = []
	for i in range(gameNumber-1, gameNumber-1-numberOfGamesToGetAverageFor, -1):
		pastRowsToGetAverageFor.append(rawStats[i])

	return pastRowsToGetAverageFor


def getRawStats():

	fileName = '../rawGameStatsAndInfo/' + str(YEAR) + '/ATL-' + str(YEAR) + '.txt'
	f = open(fileName)

	rawStatList = []
	for row in f:
		row = row.strip('\n')
		rawStatList.append(row)

	f.close()

	return rawStatList


def getListOfStats():

	listOfStats = []
	fileName = '../rawGameStatsAndInfo/glossary.txt'
	f = open(fileName)
	for line in f:
		statName = line.strip('\n')
		listOfStats.append(statName)

	f.close()

	return listOfStats


main()