import sys
sys.path.append("..") # Adds higher directory to python modules path.
from constants import *

def createTheDataModel(averagesToGet):
	if len(averagesToGet) == 0:
		return None

	averagesToGet.sort(reverse=True)

	theDataModel = []
	for YEAR in [2013, 2014]:

		teamInitials = getListOfTeamInitials(YEAR)
		for teamInitial in teamInitials:
			allAveragedRows = getRowsForAllAveragesToGet(averagesToGet, teamInitial, YEAR)
			combinedAveragesRows = combineAllAveragesIntoRowsBasedOnDates(averagesToGet, allAveragedRows)

			for row in combinedAveragesRows:
				formattedRows = seperateInputsFromOutputs(row)
				theDataModel.append(formattedRows)

	return theDataModel	


def seperateInputsFromOutputs(row):
	homeOrAway = row[INDEX_OF_NEURAL_NETWORK_HOME_OR_AWAY]
	if homeOrAway == 'Home':
		homeOrAway = 1
	else:
		homeOrAway = 0

	output = row[INDEX_OF_NEURAL_NETWORK_RESULT_STRAIGHT_UP]
	if output == 'W':
		output = [1]
	else:
		output = [0]

	inputs = [homeOrAway] + row[INDEX_OF_BACK_TO_BACK_INFO:]
	inputs = [homeOrAway] + inputs

	makeAllInputsNumbers(inputs)

	return [tuple(inputs), tuple(output)]

def makeAllInputsNumbers(inputs):

	for i in range(len(inputs)):
		inputs[i] = float(inputs[i])



def combineAllAveragesIntoRowsBasedOnDates(averagesToGet, allAveragedRows):
	largestAverage = averagesToGet[0]
	firstGameNumberAllFilesContain = allAveragedRows[largestAverage][0][0]

	allAveragesForEachGameNumber = {}
	for number in averagesToGet:
		seasonStats = allAveragedRows[number]
		for row in seasonStats:
			gameNumber = row[0]

			try:
				averagedStats = allAveragesForEachGameNumber[gameNumber]
				allAveragesForEachGameNumber[gameNumber] = averagedStats + row[INDEX_OF_FIRST_STAT_TO_ADD_TO_NEURAL_NETWORK:]
			except:
				allAveragesForEachGameNumber[gameNumber] = row

	combinedAveragesRows = []
	gameNumber = int(firstGameNumberAllFilesContain)
	while True:
		if str(gameNumber) not in allAveragesForEachGameNumber:
			break
		combinedAveragesRows.append(allAveragesForEachGameNumber[str(gameNumber)])
		gameNumber += 1

	return combinedAveragesRows


def getRowsForAllAveragesToGet(averagesToGet, teamInitial, YEAR):

	rowsToAverage = {}
	for averageToGet in averagesToGet:
		fileName = getFileName(averageToGet, teamInitial, YEAR)
		averagedStats = getStatsFromFile(fileName)
		rowsToAverage[averageToGet] = averagedStats

	return rowsToAverage


def getStatsFromFile(fileName):

	f = open(fileName)

	averageStats = []
	for row in f:
		row = row.strip('\n')
		row = row.split(', ')
		averageStats.append(row)

	f.close()

	return averageStats

def getFileName(averageToGet, teamInitial, YEAR):

	fileName = '../format_data_for_neural_nets/' + str(YEAR) + '/' + teamInitial + '/'
	fileName += teamInitial + '-Combined-' + str(averageToGet) + '-GameAverages.txt'
	return fileName


# Note 1: Charlotte is CHA when year <= 2014, and CHO otherwise
# Note 2: New Orleans is NOH when year <= 2013, and NOP otherwise
def getListOfTeamInitials(YEAR):

	listOfTeamInitials = []
	f = open("../data_collection_and_storage/rawGameStatsAndInfo/teamInitials.txt", 'r')
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


averagesToGet = [3,9,18]
createTheDataModel(averagesToGet)