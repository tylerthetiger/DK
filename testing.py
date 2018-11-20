from nba_api.stats.static import players
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
        return (self.name + ', ' + self.position + ', ' + self.avgPoints + ', ' + self.salary)
    def __str__(self):
        return (self.name + ', ' + self.position + ', ' + self.avgPoints + ', ' + self.salary)
    
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
    eligiblePlayers = GetListOfPlayers("./DKSalaries.csv")
    for player in eligiblePlayers:
        print player
    #print GetNBAId("Kevin Love")
if __name__=="__main__":
    main()