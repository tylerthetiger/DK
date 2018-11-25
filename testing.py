from nba_api.stats.static import players
from datetime import datetime,timedelta
from basketball_reference_web_scraper import client
from player import Player,getLastTwoWeeksAveragePoints, GetEligiblePlayers,GetProjection
import csv
import datetime


def getBoxScoreForPlayer(playerObj):
    playerName = playerObj.name
    dateToPull=(datetime.datetime.now() - datetime.timedelta(1))
    yesterdayGames = client.player_box_scores(day=dateToPull.day, month=dateToPull.month, year=dateToPull.year)
    for boxscore in yesterdayGames:
        if boxscore['name'] in playerName or playerName in boxscore['name']:
            return boxscore
    return None



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
        score = getBoxScoreForPlayer(player)
        fantasyPoints = FantasyScoreFromSingleGame(score)
        breakoutScore = avgScore * 1.25
    #determine if breakout game
        if fantasyPoints == 0:
            pass 
        elif fantasyPoints >= breakoutScore:
            breakOutPlayers.append(player)
        else:
            pass
    #put in list if breakout game
    return breakOutPlayers
    # return avgScore

def main():
    eligibleList = GetEligiblePlayers('DKSalaries-Nov25.csv', 'injuries.csv')
    GetProjection(eligibleList)
    for player in eligibleList:
        print(player)


    # print(eligibleList)
    # player = getBoxScoreForPlayer("Tobias Harris")
    # fantasyPoints = FantasyScoreFromSingleGame(player)
    # print fantasyPoints
    # eligiblePlayers = GetListOfPlayers("./DKSalaries.csv")
    # print GetNBAId("Kevin Love")
if __name__=="__main__":
    main()