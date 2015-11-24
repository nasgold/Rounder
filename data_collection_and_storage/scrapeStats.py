import re
import urllib2,sys
import time
import datetime
from bs4 import BeautifulSoup, NavigableString

YEAR = 2015
GAMBLING_YEAR = str(YEAR-1) + "-" + str(YEAR)

def main():

	baseUrl = "http://www.basketball-reference.com/teams/"

	listOfTeamInitials = getListOfTeamInitials()
	listOfGameStatUrls = generateGameStatUrls(baseUrl, listOfTeamInitials)

	for gameStatUrl in listOfGameStatUrls[0:1]:
		gameStatRows = getGameStatRowsFromTable(gameStatUrl)
		formattedGameStatRows = formatRowsAsLists(gameStatRows)

		# Get all gambling results and spreads for each game
		# gamblingInfoRows is a list (length 82) of the following format: result against the spread, the line (e.g. [(W, -5), (L, 2), etc.]
		gamblingInfoRows = getGamblingInfo(gameStatUrl)
		completeRows = addGamblingInfoToEachRow(gamblingInfoRows, formattedGameStatRows)

		# Get rid of the stats we don't want (e.g. any percentage stat), remove None values, and rename the home/away stat
		polishedRows = filterAndCleanRows(completeRows)

		saveAsTextFile(gameStatUrl, polishedRows)


def filterAndCleanRows(completeRows):

	# When counter == 0: we are removing a redundant game number (the first 2 columns are identical)
	# When counter == 10, 13, or 16: we are removing the team's percentage stats (e.g. FG%, FT%, etc)
	# When counter == 24: we are removing a column of all None (the reason it is there is so the table looks nice)
	# When counter == 27, 30, or 33: we are removing the oppentents's percentage stats (e.g. FG%, FT%, etc)

	irrelevantStatIndexes = [0, 10, 13, 16, 24, 27, 30, 33] 

	polishedRows = []
	for row in completeRows:
		polishedRow = []
		counter = 0
		for stat in row:
			
			# Format home and away (stat will equal either @ or None)
			if counter == 3:
				if stat == "@":
					stat = "Away"
				else:
					stat = "Home"

			# Add all relevant stats to the polished row
			if counter not in irrelevantStatIndexes:
				polishedRow.append(stat)

			counter += 1

		polishedRows.append(polishedRow)

	return polishedRows


def addGamblingInfoToEachRow(gamblingInfoRows, formattedGameStatRows):

	completeRows = []
	counter = 0
	for statRow in formattedGameStatRows:
		statRow.append(gamblingInfoRows[counter][0])
		statRow.append(gamblingInfoRows[counter][1])

		completeRows.append(statRow)
		counter += 1

	return completeRows


def getGamblingInfo(gameStatUrl):

	teamInitial = getTeamInitial(gameStatUrl)
	teamId = getTeamId(teamInitial)
 
	gamblingUrl = "http://www.covers.com/pageLoader/pageLoader.aspx?page=/data/nba/teams/pastresults/" + GAMBLING_YEAR + "/team" + teamId + ".html"
	
	html = urllib2.urlopen(gamblingUrl)
	soup = BeautifulSoup(html)
	gamblingTable = soup.findAll('table', attrs={'class' : 'data'})
	
	
	if len(gamblingTable) == 2: # made the playoffs, so 2 tables are on the page (the first of which is the playoff table)
		gamblingStatTable = gamblingTable[1]
	else:
		gamblingStatTable = gamblingTable[0]

	rows = gamblingStatTable.findChildren(['tr'])
	rows = formatRowsAsLists(rows)

	resultList = []
	spreadList = []
	for row in rows:
		resultAndSpread = row[4].strip('\r\n        ')
		resultAndSpread = resultAndSpread.split(" ")
		resultList.append(resultAndSpread[0])
		spreadList.append(resultAndSpread[1])
	
	# Reverse because the table starts at game 82, we want it to start at game 1
	resultList.reverse()
	spreadList.reverse()

	gamblingInfoList = []
	for i in range(len(resultList) -1):  # subtracting 1 to remove table header from gamblingInfoList
		gameInfo = (resultList[i], spreadList[i])
		gamblingInfoList.append(gameInfo)

	return gamblingInfoList


def getTeamId(teamInitial):

	f = open("teamIds.txt", 'r')
	for line in f:
		line = line.strip('\n')
		line = line.split(", ")
		lineInitial = line[0]
		lineId = line[1]

		if lineInitial == teamInitial:
			f.close()
			return lineId

	f.close()
	raise ValueError('Could not get team id. This should never happen.')
	return teamId


def getTeamInitial(url):

	url = url.split('teams')
	teamInitial = url[1][1:4]
	return teamInitial


def saveAsTextFile(url, formattedGameRows):

	teamInitial = getTeamInitial(url)
	fileName = str(YEAR) + "/" + teamInitial + ".txt"

	f = open(fileName, 'w')
	for row in formattedGameRows:
		formattedRow = ""
		for stat in row:
			formattedRow += str(stat) + ", "

		formattedRow = formattedRow[:-2] + "\n"

		f.write(formattedRow)

	f.close()


def formatRowsAsLists(rows):

	allRows = []
	for row in rows:
		formattedRow = []
		cells = row.findChildren('td')
		if len(cells) == 0:
			continue

		for cell in cells:
			value = cell.string
			formattedRow.append(str(value))

		allRows.append(formattedRow)

	return allRows


def getGameStatRowsFromTable(gameStatUrl):
	
	html = urllib2.urlopen(gameStatUrl)
	soup = BeautifulSoup(html)

	statTable = soup.findAll('table', attrs={'id' : 'tgl_basic'})
	statTable = statTable[0]
	rows = statTable.findChildren(['tr'])

	return rows


# Example url: http://www.basketball-reference.com/teams/WAS/2015/gamelog/
def generateGameStatUrls(baseUrl, listOfTeamInitials):

	urlList = []
	for teamInitial in listOfTeamInitials:
		url = baseUrl + teamInitial + "/" + str(YEAR) + "/gamelog"
		urlList.append(url)

	return urlList


# Note 1: Charlotte is CHA when year <= 2014, and CHO otherwise
# Note 2: New Orleans is NOH when year <= 2013, and NOP otherwise
def getListOfTeamInitials():

	listOfTeamInitials = []
	f = open("teamInitials.txt", 'r')
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

