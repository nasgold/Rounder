
#Note: we use the year to read from our text files. This means 2015 is the year player during 2014/2015
YEAR = 2013

def main():

	teamInitials = getListOfTeamInitials()

	for teamInitial in teamInitials: 

		#Get the current teams raw stats from the text file generaged by scrapeAndSaveStats.py
		rawStats = getRawStatsFromTextFile(teamInitial)

		for numberOfGamesToGetAverageFor in range(1,21):
			accumulativeGameStats = accumulateStats(numberOfGamesToGetAverageFor, rawStats)			
			completeAveragedStats = averageAccumulativeGameStats(accumulativeGameStats, numberOfGamesToGetAverageFor)
			saveAveragedStats(teamInitial, numberOfGamesToGetAverageFor, completeAveragedStats)


def saveAveragedStats(team, numberOfGamesToGetAverageFor, completeAveragedStats):

	filePath = str(YEAR) + "/"
	fileName = filePath + team + "/" + team + "-" + str(numberOfGamesToGetAverageFor) + "-GameAverage.txt"

	f = open(fileName, 'w')
	for row in completeAveragedStats:
		formattedRow = ""
		for stat in row:
			formattedRow += str(stat) + ", "

		formattedRow = formattedRow[:-2] + "\n"

		f.write(formattedRow)

	f.close()

def averageAccumulativeGameStats(accumulativeGameStats, numberOfGamesToGetAverageFor):

	averagedStats = []
	for row in accumulativeGameStats:
		gameAveragedStats = []

		# Directly append the stats that can't be averaged (e.g. opponent, date, resutls, gambling lines, etc.)
		for stat in row[:10]:
			gameAveragedStats.append(stat)

		# Loop through and average the rest of the stats
		for stat in row[10:]:
			stat = stat / float(numberOfGamesToGetAverageFor)
			stat = int((stat * 100) + 0.5) / 100.0 # Adding 0.5 rounds it up. Only get 2 digits after the decimal
			gameAveragedStats.append(stat)

		averagedStats.append(gameAveragedStats)

	return averagedStats


def accumulateStats(numberOfGamesToGetAverageFor, rawStats):

	accumulativeGameStats = []
	for gameNumber in range(numberOfGamesToGetAverageFor, len(rawStats)):
		currentRow = rawStats[gameNumber]
		rowInfo = getRowInfo(currentRow)

		pastRowsToGetAverageFor = getPastRowsToAverage(numberOfGamesToGetAverageFor, rawStats, gameNumber)

		accumulatedPastStats = accumulatePastRows(pastRowsToGetAverageFor)
		finalAccumulatedGameRows = rowInfo + accumulatedPastStats

		accumulativeGameStats.append(finalAccumulatedGameRows)

	return accumulativeGameStats

def getRowInfo(currentRow):
	# Row info are the stats we won't average (see getIndexesNotToGetTheAverageFor to these stats)

	currentRow = currentRow.split(', ')

	statIndexesNotToAverage = getIndexesNotToGetTheAverageFor()
	infoStats = []
	for index in range(len(currentRow)):
		if index in statIndexesNotToAverage:
			infoStats.append(currentRow[index])

	return infoStats


def accumulatePastRows(pastRowsToGetAverageFor):

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

	# summedPastStats is a dictionary of the following form...
	# key: stat index.
	# value: the value of each stat (with that index) for each row in pastRowsToGetAverageFor

	#We are looping over summedPastStats and appending an int(key), which effectively 
	#allows us to sort the dictionary by stat order when we keyList.sort()
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