import csv
import datetime
import time
from nba_api.stats.endpoints import commonplayerinfo, playerfantasyprofile, playergamelog, teamgamelog, leaguegamelog
from nba_api.stats.static import players, teams
from basketball_reference_web_scraper import client,data #needed for team abbrevation mapping
# create a dicionary mapping city abbr to city name for defensive rankings
teamMapping = dict()

#get the 2019 schedule from basketball reference.  Only do this once!
schedule_2019 = client.season_schedule(season_end_year=2019)
yesterday=(datetime.datetime.now() - datetime.timedelta(1))
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
def teamBacktoBack_bballreference(teamAbbr):
	teamName = data.TEAM_ABBREVIATIONS_TO_TEAM[teamAbbr].value
	#check to see if a team is on a back-to-back, return True or False
	for game in schedule_2019:
		#print game
		gameStartTime = game['start_time']
		if game['home_team'].value == teamName or game['away_team'].value == teamName:
			if gameStartTime.year == yesterday.year and gameStartTime.month == yesterday.month and gameStartTime.day == yesterday.day:
				print game
				return True
	return False
def teamBacktoBack(teamAbbr):
	nba_team = teams.find_team_by_abbreviation(teamAbbr)
	print(teamAbbr)
	teamId = nba_team['id']

	date=(datetime.datetime.now() - datetime.timedelta(1)).strftime('%m/%d/%Y')
	# date = '11/23/2018'
	season = '2018-19'
	seasonType = 'Regular Season'
	attempts=0
	while attempts<5:
		try:
			gamelog = teamgamelog.TeamGameLog(season_all=season,season_type_all_star=seasonType,team_id=teamId,date_to_nullable=date,date_from_nullable=date)
			break
		except:
			print 'nba api timed out, waiting 10 minutes then trying again.  (Attempt {} of 5'.format(attempts)
			attempts+=1
			time.sleep(600)
	gameLogDf=gamelog.get_data_frames()[0]
	entry = len(gameLogDf)
	if entry == 1:
		return True
	else:
		return False
	# print(entry)

class Team:
	def __init__(self,row):
		self.name = row[1]
		self.homeRanking = row[5]
		self.awayRanking = row[6]
		self.nextGameDefensiveRating = -1 #this is the normalized defensive ranking for this team
		# lineCount=0
		# foundTeam = False
		# with open('defensive_ranking.csv') as csv_file:
		# 	csv_reader = csv.reader(csv_file, delimiter='\t')
		# 	for row in csv_reader:
		# 		if lineCount == 0:
		# 			lineCount+=1 #skip the header
		# 		else:
		# 			if row[1] == teamMapping[row[1]]:
		# 				#matched the team we are looking for
		# 				foundTeam = True
		# 				self.homeRanking = row[5]
		# 				self.awayRanking = row[6]

		# if foundTeam == False:
		# 	print 'couldnt find team'
		# 	raise Exception

	def __repr__(self):
		return 'Team({},{},{},{})'.format(self.name,self.homeRanking,self.awayRanking,self.nextGameDefensiveRating)
	def __str__(self):
		return '{},{},{},{}'.format(self.name,self.homeRanking,self.awayRanking,self.nextGameDefensiveRating)

def getListOfTeams(csvFileName):
    listOfTeams = []
    lineCount=0
    with open(csvFileName) as csv_file:
       csv_reader = csv.reader(csv_file, delimiter='\t')
       for row in csv_reader:
            if lineCount == 0:
                lineCount+=1 #skip the header
            else:
                #TODO addd the actual nba player id not the draft kings ID
                tempTeamObj=Team(row)
                listOfTeams.append(tempTeamObj)
    return listOfTeams

# get whether todays game is home or away
def getTeamAway(csvFileName):
	awayTeam = []
	today=datetime.datetime.today().strftime('%b %d %Y')
	lineCount=0
	with open(csvFileName) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			if lineCount == 0:
				lineCount+=1 #skip the header
			else:
				if today in row[0] or row[0] in today:
					awayTeam.append(row[4])
				else:
					pass
	return awayTeam

def getTeamHome(csvFileName):
	homeTeam = []
	today=datetime.datetime.today().strftime('%b %d %Y')
	lineCount=0
	with open(csvFileName) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			if lineCount == 0:
				lineCount+=1 #skip the header
			else:
				if today in row[0] or row[0] in today:
					homeTeam.append(row[2])
				else:
					pass
	return homeTeam

# find deviation from average to include in player projection
def getNextGameDefensiveRating(csvFileName):
	allTeams = getListOfTeams(csvFileName)
	homeTeam = getTeamHome('nov_schedule.csv')
	awayTeam = getTeamAway('nov_schedule.csv')
	teamOffset = dict()

	for teamobj in allTeams:
		# print team.name
		# print team.awayRanking
		for home in homeTeam:
			if teamobj.name in home:
				teamobj.nextGameDefensiveRating = teamobj.homeRanking
				homeAvg = getAverageHomeRanking('defensive_ranking.csv')
				homeOffset = float(teamobj.nextGameDefensiveRating)/homeAvg
				teamOffset[teamobj.name] = homeOffset
			else:
				pass

		for away in awayTeam:
			if teamobj.name in away:
				teamobj.nextGameDefensiveRating=teamobj.awayRanking
				awayAvg = getAverageAwayRanking('defensive_ranking.csv')
				awayOffset = float(teamobj.nextGameDefensiveRating)/awayAvg
				teamOffset[teamobj.name] = awayOffset
			else:
				pass
	return teamOffset
		# print(teamobj)

def main():
	print teamBacktoBack_bballreference('DEN')
	# awayRank = getAverageAwayRanking('defensive_ranking.csv')
	# print(awayRank)
	# team = teamBacktoBack('DEN')
	# defense = getTeamHomeAway('nov_schedule_test.csv')
	#city = getNextGameDefensiveRating('defensive_ranking.csv')
	#print(city)
if __name__ =="__main__":
	main()