from nba_api.stats.static import players
from datetime import datetime,timedelta
from basketball_reference_web_scraper import client

import csv
class Player:
    def __init__(self,name,NBAplayerID,position,avgPoints,salary):
        self.name = name
        self.NBAplayerID = NBAplayerID
        self.position = position
        self.avgPoints = avgPoints
        self.salary = salary
        self.projection = 0
    def __repr__(self):
        return 'Player({},{},{},{},{})'.format(self.name,self.NBAplayerID,self.position,self.avgPoints,self.salary,self.projection)
       # return (self.name + ', ' + self.position + ', ' + self.avgPoints + ', ' + self.salary)
    def __str__(self):
        return '{},{},{},{},{}'.format(self.name,self.NBAplayerID,self.position,self.avgPoints,self.salary,self.projection)

        #return (self.name + ', ' + self.position + ', ' + self.avgPoints + ', ' + self.salary)
    

## IN: NBAPlayerID
## Return: True if today's game will be a back-to-back, false otherwise
def BackToBack(playerName):
    yesterdayGames = client.player_box_scores(day=20, month=11, year=2018) #TODO calculate yesterday date with datetime
    for boxscore in yesterdayGames:
        if boxscore['name'] in playerName:
            return True
    return False
def FantasyScoreFromSingleGame(BoxScoreEntry):
    return 0 #TODO calculate fantasy points for a single game given a box score

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
                #TODO addd the actual nba plyaer id not the draft kings ID
                # print row[2] + " : " + row[3]
                tempPlayerObj = Player(row[2], row[3], row[4], row[8], row[5])
                listOfPlayers.append(tempPlayerObj)
    return listOfPlayers
def GetNBAId(playerFullName):
    playerObj=players.find_players_by_full_name(playerFullName)
    return playerObj[0]["id"]
def main():
    print BackToBack("Tim Hardaway Jr.")
   # eligiblePlayers = GetListOfPlayers("./DKSalaries.csv")
   # for player in eligiblePlayers:
   #     print player
    #print GetNBAId("Kevin Love")
if __name__=="__main__":
    main()
