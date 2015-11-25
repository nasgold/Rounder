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

		# GamblingInfoRows is a list (length 82) of the following format:
		# result against the spread, the line, result against the over/under, and the over/under line (e.g. [(W, -5, U, 205), etc...]
		gamblingInfoRows = getGamblingInfo(gameStatUrl)
		statAndGamblingRows = addGamblingInfoToEachRow(gamblingInfoRows, formattedGameStatRows)

		# Add whether the team is played the previous day (0 if they didn't, 1 if they did)
		completeRows = addWhetherTeamPlayedOnThePreviousDay(statAndGamblingRows)

		# Get rid of the stats we don't want (e.g. any percentage stat), remove None values, and rename the home/away stat
		polishedRows = filterAndCleanRows(completeRows)

		saveAsTextFile(gameStatUrl, polishedRows)

def addWhetherTeamPlayedOnThePreviousDay(statAndGamblingRows):

	statAndGamblingRows[0].append(0) # did not play the previous day, so adding a 0 here.

	firstGamePlayed = statAndGamblingRows[0][2]
	dateOfPreviousGame = datetime.datetime.strptime(firstGamePlayed,"%Y-%m-%d")

	completeRows = []
	for row in statAndGamblingRows[1:]: # starting at the second game (already added a 0 for the first game)
		dateOfGame = datetime.datetime.strptime(row[2],"%Y-%m-%d")
		dayBeforeGame = dateOfGame - datetime.timedelta(days=1)

		# Add a 1 or 0 to the row
		if dayBeforeGame == dateOfPreviousGame:
			row.append(1)
		else:
			row.append(0)

		dateOfPreviousGame = dateOfGame
		completeRows.append(row)


	return completeRows


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
		relatedGamblingRow = gamblingInfoRows[counter]
		for gamblingStat in relatedGamblingRow:
			statRow.append(gamblingStat)

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

	spreadResultList = []
	pointSpreadList = []

	overUnderResultList = []
	overUnderLineList = []
	for row in rows[1:]: #first row is the header of the table, so we can skip it

		#Get info associated with the spread
		speadInfo = row[4].strip('\r\n        ')
		speadInfo = speadInfo.split(" ")
		spreadResultList.append(speadInfo[0])
		pointSpreadList.append(speadInfo[1])

		#Get info associated with the over/under
		overUnderInfo = row[5].strip('\r\n        ')
		overUnderInfo = overUnderInfo.split(" ")
		overUnderResultList.append(overUnderInfo[0])
		overUnderLineList.append(overUnderInfo[1])

	
	# Reverse because the table starts at game 82, but we want it to start at game 1
	spreadResultList.reverse()
	pointSpreadList.reverse()
	overUnderResultList.reverse()
	overUnderLineList.reverse()

	gamblingInfoList = []
	for i in range(len(spreadResultList)):
		gameInfo = (spreadResultList[i], pointSpreadList[i], overUnderResultList[i], overUnderLineList[i])
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

