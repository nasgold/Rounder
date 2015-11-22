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
	listOfUrls = generateUrls(baseUrl, listOfTeamInitials)

	for url in listOfUrls[0:1]:
		gameRows = getGameRowsFromTable(url)
		formattedGameRows = formatRowsAsLists(gameRows)

		#formattedGameRows = []
		#addGamblingInfoToEachRow(url, formattedGameRows)


		saveAsTextFile(url, formattedGameRows)
		

def addGamblingInfoToEachRow(url, formattedGameRows):

	teamInitial = getTeamInitial(url)
	teamId = getTeamId(teamInitial)
 
	gamblingUrl = "http://www.covers.com/pageLoader/pageLoader.aspx?page=/data/nba/teams/pastresults/" + GAMBLING_YEAR + "/team" + teamId + ".html"
	
	html = urllib2.urlopen(gamblingUrl)
	soup = BeautifulSoup(html)
	gamblingTable = soup.findAll('table', attrs={'class' : 'data'})
	
	
	if len(gamblingTable) == 2: #made the playoffs, so 2 tables are on the page (the first of which is the playoff table)
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
	
	# Reverse because the table starts at game 82
	resultList.reverse()
	spreadList.reverse()
	print resultList
	print spreadList

	

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


def formatRowsAsLists(gameRows):

	allRows = []
	for row in gameRows:
		formattedRow = []
		cells = row.findChildren('td')
		if len(cells) == 0:
			continue

		for cell in cells:
			value = cell.string
			formattedRow.append(str(value))

		allRows.append(formattedRow)

	return allRows


def getGameRowsFromTable(url):
	
	html = urllib2.urlopen(url)
	soup = BeautifulSoup(html)

	statTable = soup.findAll('table', attrs={'id' : 'tgl_basic'})
	statTable = statTable[0]
	rows = statTable.findChildren(['tr'])
	return rows


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


# Example url: http://www.basketball-reference.com/teams/WAS/2015/gamelog/
def generateUrls(baseUrl, listOfTeamInitials):

	urlList = []
	for teamInitial in listOfTeamInitials:
		url = baseUrl + teamInitial + "/"
		url += str(YEAR) + "/gamelog"
		urlList.append(url)

	return urlList

main()


