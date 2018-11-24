# do defensive stuff only, maybe integrate offensive rating later
#first you need to create a dictionary mapping of team abbrev to teamname as csv lists it
#that way you can do a quick lookup and match in your for loop below
#teamabbrev will be GS (as draftkings csv lists it)
#you're doing a list, we want to do a dict
#also i would do it outside of the class as a global so we don't have to create the dict every time we make a new Team class
import csv
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
	#	print "Avg away ranking: {}".format(avgRanking)
		return avgRanking

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
	awayRank = getAverageAwayRanking('defensive_ranking.csv')
	print(awayRank)
if __name__ =="__main__":
	main()