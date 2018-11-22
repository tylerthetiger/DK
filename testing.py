from nba_api.stats.static import players
from datetime import datetime,timedelta
from basketball_reference_web_scraper import client
from player import Player
import csv

## IN: NBAPlayerID
## Return: True if today's game will be a back-to-back, false otherwise
def BackToBack(playerName):
    yesterdayGames = client.player_box_scores(day=21, month=11, year=2018) #TODO calculate yesterday date with datetime
    for boxscore in yesterdayGames:
        if boxscore['name'] == playerName:
            return True
    return False

def getBoxScoreForPlayer(playerName):
    yesterdayGames = client.player_box_scores(day=21, month=11, year=2018) #TODO calculate yesterday date with datetime
    for boxscore in yesterdayGames:
        if boxscore['name'] in playerName:
            return boxscore
    return None

def FantasyScoreFromSingleGame(boxscore):
    #TODO calculate fantasy points for single game
    # print boxscore
    try:
        freeThrowsMade = (boxscore['made_free_throws'])
    except:
        freeThrowsMade = 0
    try:
        twoPointsMade = (boxscore['made_field_goals'] - boxscore['made_three_point_field_goals'])
    except:
        twoPointsMade = 0
    try:
        threePointsMade = (boxscore['made_three_point_field_goals'])
    except:
        threePointsMade = 0
    try:
        totalPoints = (freeThrowsMade * 1) + (twoPointsMade * 2) + (threePointsMade * 3)
    except:
        totalPoints = 0
    try:
        rebounds = (boxscore['defensive_rebounds'] + boxscore['offensive_rebounds'])
    except:
        rebounds = 0
    try:
        assists = (boxscore['assists'])
    except: 
        assists = 0
    try:
        steals = (boxscore['steals'])
    except:
        steals = 0
    try:
        blocks = (boxscore['blocks'])
    except:
        blocks = 0
    try:
        turnovers = (boxscore['turnovers'])
    except:
        turnovers = 0

    totalFantasyScore = (twoPointsMade * 2) + (threePointsMade * 3.5) + (rebounds * 1.25) \
                        + (assists * 1.5) + (steals * 2) + (blocks * 2) + (turnovers * -0.5) \
                        + (freeThrowsMade * 1)
  

    #calculate if the player scored double double
    twoDigitStats = 0

    if totalPoints >= 10:
        twoDigitStats += 1
    if rebounds >= 10:
        twoDigitStats += 1
    if assists >= 10:
        twoDigitStats += 1 
    if steals >= 10:
        twoDigitStats += 1
    if blocks >= 10:
        twoDigitStats += 1
    if twoDigitStats >= 2:
        totalFantasyScore += 1.5
    if twoDigitStats >= 3:
        totalFantasyScore += 3

    return totalFantasyScore

def GetListOfPlayers(csvFileName):
    listOfPlayers = []
    lineCount=0
    with open(csvFileName) as csv_file:
#Position,Name + ID,Name,ID,Roster Position,Salary,Game Info,TeamAbbrev,AvgPointsPerGame
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if lineCount == 0:
                lineCount+=1 #skip the header
            else:
                #TODO addd the actual nba player id not the draft kings ID
                # print row[2] + " : " + row[3]
                tempPlayerObj = Player(row[2], row[3], row[4], row[8], row[5])
                listOfPlayers.append(tempPlayerObj)
    return listOfPlayers

def GetNBAId(playerFullName):
    playerObj=players.find_players_by_full_name(playerFullName)
    return playerObj[0]["id"]

def BreakOutGame(listOfPlayers):
    breakOutPlayers = []
    #loop through players in DK Salaries
    for player in listOfPlayers: 
    #get average scores
        avgScore = float(player.avgPoints)
        name = player.name
    #calculate Fantasy Score
        score = getBoxScoreForPlayer(name)
        fantasyPoints = FantasyScoreFromSingleGame(score)
        breakoutScore = avgScore * 1.25
    #determine if breakout game
        if fantasyPoints == 0:
            pass 
        elif fantasyPoints >= breakoutScore:
            tempBreakOut = (name, fantasyPoints)
            breakOutPlayers.append(tempBreakOut)
        else:
            pass
    #put in list if breakout game
    return breakOutPlayers
    # return avgScore

def main():
    # print BackToBack("John Wall")
    allPlayers = GetListOfPlayers('DKSalaries.csv')
    breakOut = BreakOutGame(allPlayers)
    print(breakOut)
    # player = getBoxScoreForPlayer("Tobias Harris")
    # fantasyPoints = FantasyScoreFromSingleGame(player)
    # print fantasyPoints
   # eligiblePlayers = GetListOfPlayers("./DKSalaries.csv")
   # for player in eligiblePlayers:
   #     print player
    #print GetNBAId("Kevin Love")
if __name__=="__main__":
    main()