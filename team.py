import csv
import datetime
from nba_api.stats.endpoints import commonplayerinfo, playerfantasyprofile, playergamelog, teamgamelog
from nba_api.stats.static import players, teams
# create a dicionary mapping city abbr to city name for defensive rankings
teamMapping = dict()

#need to iterate through CSV
with open('teammapping.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	lineCount = 0
	for row in csv_reader:
		if lineCount == 0:
			lineCount+=1 #skip the header
		else:
			teamCity = row[0]
			teamAbbr = row[1]
			teamMapping[teamAbbr] = teamCity
	
def getAverageHomeRanking(csvFileName):
	with open(csvFileName) as csv_file:
		csv_reader = csv.reader(csv_file,delimiter='\t')
		lineCount=0
		numTeams = 0
		totalValue = float(0)
		for row in csv_reader:
			if lineCount==0:
				lineCount+=1
			else:
				# print row
				numTeams+=1
				totalValue+=float(row[5])
	if numTeams == 0:
		print 'unable to parse csv correctly'
		raise Exception
	else:
		avgRanking = totalValue/numTeams
		#print "Avg home ranking: {}".format(avgRanking)
		return avgRanking

def getAverageAwayRanking(csvFileName):
	with open(csvFileName) as csv_file:
		csv_reader = csv.reader(csv_file,delimiter='\t')
		lineCount=0
		numTeams = 0
		totalValue = float(0)
		for row in csv_reader:
			if lineCount==0:
				lineCount+=1
			else:
				# print row
				numTeams+=1
				totalValue+=float(row[6])
	if numTeams == 0:
		print 'unable to parse csv correctly'
		raise Exception
	else:
		avgRanking = totalValue/numTeams
		return avgRanking

def teamBacktoBack(teamAbbr):
	nba_team = teams.find_team_by_abbreviation(teamAbbr)
	teamId = nba_team['id']

	date=(datetime.datetime.now() - datetime.timedelta(1)).strftime('%m/%d/%Y')
	# date = '11/23/2018'
	season = '2018-19'
	seasonType = 'Regular Season'

	gamelog = teamgamelog.TeamGameLog(season_all=season,season_type_all_star=seasonType,team_id=teamId,date_to_nullable=date,date_from_nullable=date)
	gameLogDf=gamelog.get_data_frames()[0]
	entry = len(gameLogDf)
	if entry == 1:
		return True
	else:
		return False
	# print(entry)

class Team:
	def __init__(self,teamabbrev):
		lineCount=0
		foundTeam = False
		with open('defensive_ranking.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter='\t')
			for row in csv_reader:
				if lineCount == 0:
					lineCount+=1 #skip the header
				else:
					if row[1] == teamMapping[teamabbrev]:
						#matched the team we are looking for
						foundTeam = True
						self.homeRanking = row[5]
						self.awayRanking = row[6]

		if foundTeam == False:
			print 'couldnt find team'
			raise Exception

def main():
	# awayRank = getAverageAwayRanking('defensive_ranking.csv')
	# print(awayRank)
	team = teamBacktoBack('DEN')
	print(team)
if __name__ =="__main__":
	main()