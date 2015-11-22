mport re
import urllib2,sys
import time
import datetime
from bs4 import BeautifulSoup, NavigableString

YEAR = 2015

def main():

	baseUrl = "http://www.basketball-reference.com/teams/"

	listOfTeamInitials = getListOfTeamInitials()
	listOfUrls = generateUrls(baseUrl, listOfTeamInitials)

	for url in listOfUrls[0:1]:
		gameRows = getGameRowsFromTable(url)
		formattedRows = formatRowsAsTuples(gameRows)
		for dude in formattedRows:
			print dude
		insertRowsIntoTable(gameRows)


def formatRowsAsTuples(gameRows):

	allRows = []
	for row in gameRows:
		formattedRow = []
		cells = row.findChildren('td')
		if len(cells) == 0:
			continue

		for cell in cells:
			value = cell.string
			formattedRow.append(str(value))

		formattedRow = tuple(formattedRow)
		allRows.append(formattedRow)

	return allRows


def getGameRowsFromTable(url):
	
	html = urllib2.urlopen(url)
	soup = BeautifulSoup(html)

	statTable = soup.findAll('table', attrs={'id' : 'tgl_basic'})
	statTable = statTable[0]
	rows = statTable.findChildren(['tr'])
	return rows


#Note 1: Charlotte is CHA when year <= 2014, and CHO otherwise
#Note 2: New Orleans is NOH when year <= 2013, and NOP otherwise
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

	return listOfTeamInitials


#Exmple url: http://www.basketball-reference.com/teams/WAS/2015/gamelog/
def generateUrls(baseUrl, listOfTeamInitials):

	urlList = []
	for teamInitial in listOfTeamInitials:
		url = baseUrl + teamInitial + "/"
		url += str(YEAR) + "/gamelog"
		urlList.append(url)

	return urlList

main()


