import csv
import datetime
import time
#from player import *
from nba_api.stats.endpoints import commonplayerinfo, playerfantasyprofile, playergamelog, teamgamelog, leaguegamelog
from nba_api.stats.static import players, teams
from basketball_reference_web_scraper import client,data #needed for team abbrevation mapping


# get data from web instead of csv
def GetInjuriesv2():
    injuries = client.injury_report()
    injuredPlayers = []

    for injuredPlayer in injuries:
        injuredPlayers.append(injuredPlayer['player'])
    
    return injuredPlayers

	
# create a dicionary mapping city abbr to city name for defensive rankings
teamMapping = dict()

##TODO create a parser for https://www.basketball-reference.com/leagues/NBA_2019_ratings.html and use that for defensive ranking
#restructure all of this code to create a list of Team objects that hold all the information that Player() needs to make projections
#include a reference in the player to the Team object/list entry for the opponent and the player's team.

def getTeamPace():
	pace = client.teams_misc_stats('2019')
	teamsPace = []

	for team in pace:
		teamPace.append(team['pace'])

	return teamsPace

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
		gameStartTime = game['start_time']
		if game['home_team'].value == teamName or game['away_team'].value == teamName:
			if gameStartTime.year == yesterday.year and gameStartTime.month == yesterday.month and gameStartTime.day == yesterday.day:
				print game
				return True
	return False

# def teamBacktoBack(teamAbbr):
# 	nba_team = teams.find_team_by_abbreviation(teamAbbr)
# 	print(teamAbbr)
# 	teamId = nba_team['id']

# 	date=(datetime.datetime.now() - datetime.timedelta(1)).strftime('%m/%d/%Y')
	# date = '11/23/2018'
# 	season = '2018-19'
# 	seasonType = 'Regular Season'
# 	attempts=0
# 	while attempts<5:
# 		try:
# 			gamelog = teamgamelog.TeamGameLog(season_all=season,season_type_all_star=seasonType,team_id=teamId,date_to_nullable=date,date_from_nullable=date)
# 			break
# 		except:
# 			print 'nba api timed out, waiting 10 minutes then trying again.  (Attempt {} of 5'.format(attempts)
# 			attempts+=1
# 			time.sleep(600)
# 	gameLogDf=gamelog.get_data_frames()[0]
# 	entry = len(gameLogDf)
# 	if entry == 1:
# 		return True
# 	else:
# 		return False
	# print(entry)

class Team:
	def __init__(self,row):
		self.name = row[1]
		self.homeRanking = row[5]
		self.awayRanking = row[6]
		self.nextGameDefensiveRating = -1 

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

#TODO: get eligible players, calculate defensive ranking, assign to team
# we could make this more efficient by only getting defensive ratings of teams that are playing...this returns all
def getPlayerDefensiveRanking():
	allTeams = getListOfTeams('defensive_ranking.csv')
	playerStats = client.players_stats_per_100_poss('2019')
	injuredPlayers = GetInjuriesv2()
	eligiblePlayers = []
	finalList = []

	for allPlayers in playerStats:
		eligiblePlayers.append(allPlayers['name'])

	for eligible in eligiblePlayers:
		playerIsInjured=False
		for injured in injuredPlayers:
			if injured in eligible:
				playerIsInjured=True
          
		if playerIsInjured==False:
			finalList.append(eligible)

	team_defense = dict()
	team_defense_all = dict()

	allPlayerDefense = 0
	allPlayers = 0

	for testdefensiveRating in playerStats:
		allPlayers += 1
		if testdefensiveRating['team_abbr'] in team_defense_all:
			team = testdefensiveRating['team_abbr']
			player_defensive_rating = testdefensiveRating['defensive_rating']#the individual players rating
			(prev_defensive_avg,defensiverating_total,players) = team_defense_all[team]
			new_team_def_rating_avg = (defensiverating_total+player_defensive_rating)/(players+1)
			team_defense_all[team] = (new_team_def_rating_avg,defensiverating_total+player_defensive_rating,players+1)
		else:
			team = testdefensiveRating['team_abbr']
			# print 'creating new entry for ' + str(team)
			defensive_rating = testdefensiveRating['defensive_rating']
			team_defense_all[team] = (defensive_rating,defensive_rating,1)
	# print team_defense_all
	# print len(playerStats)
	countEligible = 0

	for defensiveRating in playerStats:
		countEligible += 1
		if defensiveRating['name'] in finalList:
			# team already exists and need to take avg of all players defensive rankings
			if defensiveRating['team_abbr'] in team_defense and defensiveRating['minutes_played'] > 0:
				#find the team in the list
				team = defensiveRating['team_abbr']
				teamCity = teamMapping[team]
				# get % of game played by player (48 min in one game)
				player_impact = (defensiveRating['minutes_played']/defensiveRating['games_played'])/48
				#get defensive rating of this one player record
				player_defensive_rating = player_impact * (defensiveRating['defensive_rating'])#the individual players rating
				#keep track of new and old rating for testing purposes
				(prev_defensive_avg,defensiverating_total,players) = team_defense[team]
				#set new ranking based on new player rating
				new_team_def_rating_avg = (defensiverating_total+player_defensive_rating)
				team_defense[teamCity] = (new_team_def_rating_avg,defensiverating_total+player_defensive_rating,players+1)
			else:
				# if team doesnt exist in list, create it
				team = defensiveRating['team_abbr']
				teamCity = teamMapping[team]
				# print 'creating new entry for ' + str(team)
				# set defensive rating for team based on first player identified
				defensive_rating = defensiveRating['defensive_rating']
				# create a tuple for the dictionary
				team_defense[teamCity] = (defensive_rating,defensive_rating,1)
		else:
			pass

	# find avg of all teams
	total_defense = 0
	for k, v in team_defense.items():
		ind_defense = v[0]
		total_defense = total_defense + ind_defense

	team_average_defense = total_defense/30
	# print(team_average_defense)

	# find offset by comparing team defense to average
	team_offset_defense = dict()
	for k, v in team_defense.items():
		# print(v[0])
		team_offset = float(v[0])/team_average_defense
		# print(team_offset)
		team_offset_defense[k] = team_offset

	for teamobj in allTeams:
		for teamdefense in team_offset_defense:
			if teamobj.name in teamdefense:
				teamobj.nextGameDefensiveRating = team_offset_defense[teamdefense]

	return team_offset_defense


#deprecated in favor of get defensive ranking by player
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

def main():
	# test = getPlayerDefensiveRanking()
	# print(test)
	# defenseRanking = getPlayerDefensiveRanking()
	# print defenseRanking
	# defenseOffset = defenseRanking[teamCity]
	team_pace = getTeamPace()
	print(team_pace)
	# print teamBacktoBack_bballreference('DEN')
	# awayRank = getAverageAwayRanking('defensive_ranking.csv')
	# print(awayRank)
	# team = teamBacktoBack('DEN')
	# defense = getTeamHomeAway('nov_schedule_test.csv')
	# city = getNextGameDefensiveRating('defensive_ranking.csv')
	# print(city)
if __name__ =="__main__":
	main()