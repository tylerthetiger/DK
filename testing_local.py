from testing import *
import datetime
from nba_api.stats.endpoints import commonplayerinfo, playerfantasyprofile,playergamelog
from nba_api.stats.static import players
from basketball_reference_web_scraper import client

today=datetime.datetime.today().strftime('%m/%d/%Y')
yesterday=(datetime.datetime.now() - datetime.timedelta(1)).strftime('%m/%d/%Y')
def getBoxScoreForPlayerFromLists(playerName,BoxScoreList):
    for boxscore in BoxScoreList:
        #print boxscore['name']
        #print playerName
        if playerName.lower() in boxscore['name'].lower():
            return boxscore
    return None
    
def getLastTwoWeeksAveragePoints(playerObj):
    playerName = playerObj.name
    dateIndex = 1 #counter to keep track of how many days back we are going
    totalGamesPlayed=0
    totalFantasyPoints=0
    while dateIndex<=14:
        dateToPull=(datetime.datetime.now() - datetime.timedelta(dateIndex))
        listOfGames = client.player_box_scores(day=dateToPull.day, month=dateToPull.month, year=dateToPull.year)
        currentBoxScore=getBoxScoreForPlayerFromLists(playerName,listOfGames)
        if currentBoxScore!=None:
            totalGamesPlayed+=1
            singleGameScore=FantasyScoreFromSingleGame(currentBoxScore)
            totalFantasyPoints+=singleGameScore
       # print currentBoxScore
        dateIndex+=1
    if totalGamesPlayed==0:
        print "{} played 0 games!".format(playerName)
        averagePoints=0
    else:
        averagePoints=(totalFantasyPoints/totalGamesPlayed)
    # print "{} played {} games and averaged {} points in last two weeks".format(playerName,totalGamesPlayed,averagePoints)
    return averagePoints

def main():
    getLastTwoWeeksAveragePoints("Dennis Schroder")
    return None
if __name__=="__main__":
    main()