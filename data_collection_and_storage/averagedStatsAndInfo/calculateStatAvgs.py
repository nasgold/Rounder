YEAR = 2015

def main():

	"""
	listOfStats = getListOfStats()
	for i in listOfStats:
		print i

	"""

	rawStats = getRawStats()

	for numberOfGamesToGetAverageFor in range(2,3):
		calculateGameAverages(numberOfGamesToGetAverageFor, rawStats)


def calculateGameAverages(numberOfGamesToGetAverageFor, rawStats):

	for row in rawStats[numberOfGamesToGetAverageFor:]:
		print row



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