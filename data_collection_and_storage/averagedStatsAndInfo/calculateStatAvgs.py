
YEAR = 2015

def main():

	teamInitials = getListOfTeamInitials()

	for teamInitial in teamInitials[0:1]: 

		#Get the current teams raw stats from the text file generaged by scrapeAndSaveStats.py
		rawStats = getRawStatsFromTextFile(teamInitial)

		for numberOfGamesToGetAverageFor in range(1,21):
			completeAveragedStats = calculateGameAverages(numberOfGamesToGetAverageFor, rawStats)
			saveAveragedStats(teamInitial, numberOfGamesToGetAverageFor, completeAveragedStats)


def saveAveragedStats(team, numberOfGamesToGetAverageFor, completeAveragedStats):

	fileName = team + "-" + str(numberOfGamesToGetAverageFor) + "-GameAverage"
	print fileName
	return 

	filePath
	f = open(fileName, 'w')
	for row in formattedGameRows:
		formattedRow = ""
		for stat in row:
			formattedRow += str(stat) + ", "

		formattedRow = formattedRow[:-2] + "\n"

		f.write(formattedRow)

	f.close()

def calculateGameAverages(numberOfGamesToGetAverageFor, rawStats):

	completeAveragedStats = []
	for gameNumber in range(numberOfGamesToGetAverageFor, len(rawStats)):
		currentRow = rawStats[gameNumber]
		rowInfo = getRowInfo(currentRow)

		pastRowsToGetAverageFor = getPastRowsToAverage(numberOfGamesToGetAverageFor, rawStats, gameNumber)

		averagedPastStats = averagePastRows(pastRowsToGetAverageFor)
		finalAverageRows = rowInfo + averagedPastStats

		completeAveragedStats.append(finalAverageRows)

	return completeAveragedStats

def getRowInfo(currentRow):
	# Row info are the stats we won't average (see getIndexesNotToGetTheAverageFor to these stats)

	currentRow = currentRow.split(', ')

	statIndexesNotToAverage = getIndexesNotToGetTheAverageFor()
	infoStats = []
	for index in range(len(currentRow)):
		if index in statIndexesNotToAverage:
			infoStats.append(currentRow[index])

	return infoStats


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
	# Not averaging index 5: the spread result
	# Not averaging index 6: the spread
	# Not averaging index 7: over under result
	# Not averaging index 8: over under line
	# Not averaging index 9: was this game a back to back?

	return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def getPastRowsToAverage(numberOfGamesToGetAverageFor, rawStats, gameNumber):
	pastRowsToGetAverageFor = []
	for i in range(gameNumber-1, gameNumber-1-numberOfGamesToGetAverageFor, -1):
		pastRowsToGetAverageFor.append(rawStats[i])

	return pastRowsToGetAverageFor


def getRawStatsFromTextFile(teamInitial):

	fileName = '../rawGameStatsAndInfo/' + str(YEAR) + '/' + teamInitial + '-' + str(YEAR) + '.txt'
	f = open(fileName)

	rawStatList = []
	for row in f:
		row = row.strip('\n')
		rawStatList.append(row)

	f.close()

	return rawStatList


# Note 1: Charlotte is CHA when year <= 2014, and CHO otherwise
# Note 2: New Orleans is NOH when year <= 2013, and NOP otherwise
def getListOfTeamInitials():

	listOfTeamInitials = []
	f = open("../rawGameStatsAndInfo/teamInitials.txt", 'r')
	for line in f:
		teamInitial = line.strip('\n')
		if teamInitial == 'CHO':
			if YEAR <= 2014:
				teamInitial = 'CHA'

		elif teamInitial == 'NOP':
			if YEAR <= 2013:
				teamInitial = 'NOH'

		listOfTeamInitials.append(teamInitial)

	f.close()
	return listOfTeamInitials


main()