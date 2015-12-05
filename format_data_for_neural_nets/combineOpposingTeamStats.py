import sys
sys.path.append("..") # Adds higher directory to python modules path.
from constants import *

YEAR = 2015

def main():

	teamInitials = getListOfTeamInitials()

	for numberOfGamesToGetAverageFor in range(1,21):
		allTeamsAveragedStats = getAllTeamsAveragedStats(teamInitials, numberOfGamesToGetAverageFor)

		for teamInitial in teamInitials:

			currentTeamsCombinedStats = []
			allHomeTeamAverages = allTeamsAveragedStats[teamInitial]
			for homeTeamStats in allHomeTeamAverages:
				awayTeam = getAwayTeam(homeTeamStats)
				dateOfGame = getDateOfGame(homeTeamStats)

				awayTeamStats = getAwayTeamStats(awayTeam, dateOfGame, allTeamsAveragedStats)
				if awayTeamStats != None: # Not an error, just not enough games have been played for the away team
					combinedStats = combineStatsOfBothTeams(homeTeamStats, awayTeamStats)
					currentTeamsCombinedStats.append(combinedStats)

			saveCurrentTeamsCombinedStats(teamInitial, numberOfGamesToGetAverageFor, currentTeamsCombinedStats)
			

def saveCurrentTeamsCombinedStats(teamInitial, numberOfGamesToGetAverageFor, currentTeamsCombinedStats):

	filePath = str(YEAR) + "/"
	fileName = filePath + teamInitial + "/" + teamInitial + "-Combined-" + str(numberOfGamesToGetAverageFor) + "-GameAverages.txt"

	f = open(fileName, 'w')
	for row in currentTeamsCombinedStats:
		formattedRow = ""
		for stat in row:
			formattedRow += str(stat) + ", "

		formattedRow = formattedRow[:-2] + "\n"

		f.write(formattedRow)

	f.close()


def combineStatsOfBothTeams(homeTeamStats, awayTeamStats):

	awayTeamBackToBackInfo = awayTeamStats[INDEX_OF_BACK_TO_BACK_INFO]

	# Insert awayTeamBackToBackInfo right after home teams awayTeamBackToBackInfo. By doing it like this, this info won't get
	# lost when combining game averages with each (e.g. making a row of stats-3-game-avg, stats-9-game-avg, stats-18-game-avg)
	return homeTeamStats[0:INDEX_OF_BACK_TO_BACK_INFO] + [awayTeamBackToBackInfo] + homeTeamStats[INDEX_OF_BACK_TO_BACK_INFO:] + awayTeamStats[NUMBER_OF_BASIC_STATS_NOT_TO_AVERAGE:]

def checkToMakeSureEnoughGamesHaveBeenPlayedForAwayTeams(dateOfGame, awayTeamGames):

	firstGameWeCanGetPastAveragesFor = getDateOfGame(awayTeamGames[0])
	if dateOfGame < firstGameWeCanGetPastAveragesFor:
		return False
	return True


def getAwayTeamStats(awayTeam, dateOfGame, allTeamsAveragedStats):
	
	awayTeamGames = allTeamsAveragedStats[awayTeam]

	# If the game happened before the other team has played enough games, return None.
	# For example, it's Bostons fourth game, but Dallas has only played three. We can't get the average stats
	# for Dallas over their past 3 games because they have only played 2.
	if not checkToMakeSureEnoughGamesHaveBeenPlayedForAwayTeams(dateOfGame, awayTeamGames):
		return None

	# print dateOfGame, awayTeam
	for game in awayTeamGames:
		dateOfGameForOpponent = getDateOfGame(game)
		if dateOfGame == dateOfGameForOpponent: #found the game we are looking for
			return game
	raise Exception('Could not find the date when two teams played. This should never happen.')


def getAwayTeam(game):
	return game[3]


def getDateOfGame(game):
	return game[1]


def getAllTeamsAveragedStats(teamInitials, numberOfGamesToAverage):
	allTeamsAveragedStats = {}
	for teamInitial in teamInitials:
		averagedTeamStats = getAveragedTeamStats(teamInitial, numberOfGamesToAverage)
		allTeamsAveragedStats[teamInitial] = averagedTeamStats

	return allTeamsAveragedStats


def getAveragedTeamStats(teamInitial, numberOfGamesToAverage):
	basePath = '../data_collection_and_storage/averagedStatsAndInfo/' 
	fileName = basePath + str(YEAR) + '/' + teamInitial + '/' + teamInitial + '-' + str(numberOfGamesToAverage) + '-GameAverage.txt'

	f = open(fileName)

	averageStats = []
	for row in f:
		row = row.strip('\n')
		row = row.split(', ')
		averageStats.append(row)

	f.close()

	return averageStats


# Note 1: Charlotte is CHA when year <= 2014, and CHO otherwise
# Note 2: New Orleans is NOH when year <= 2013, and NOP otherwise
def getListOfTeamInitials():

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


main()