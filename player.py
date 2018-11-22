class Player:
    def __init__(self,row):
        #name,NBAplayerID,position,avgPoints,salary,team,nextOpponent,nextGameLocation
        #row[2],row[3],row[4],row[8],row[5],row[7],opponent,location)
#opponent=getOpponent(row[6],row[7])
  #         location=getLocation(row[6],row[7])
        self.name = row[2]
        self.NBAplayerID = row[3]
        self.position = row[4]
        self.avgPoints = row[8]
        self.salary = row[5]
        self.team = row[7]
        self.nextOpponent = "nextOpponent"
        self.nextGameLocation = "nextGameLocation" #should be home or away
        self.projection = 0
    def __repr__(self):
        return 'Player({},{},{},{},{},{},{},{})'.format(self.name,self.NBAplayerID,self.position,self.avgPoints,self.salary,self.team,self.nextOpponent,self.nextGameLocation,self.projection)
       # return (self.name + ', ' + self.position + ', ' + self.avgPoints + ', ' + self.salary)
    def __str__(self):
        return '{},{},{},{},{},{},{},{}'.format(self.name,self.NBAplayerID,self.position,self.avgPoints,self.salary,self.team,self.nextOpponent,self.nextGameLocation,self.projection)

        #return (self.name + ', ' + self.position + ', ' + self.avgPoints + ', ' + self.salary)
    ###TODO fix these, this is assuming all team abbreviations are 3 letters long, doesn't hold for GS

def getLocation(gameInfo,teamAbbrev):
    team1=gameInfo[0:3]#awayteam
    team2=gameInfo[4:7]#hometeam
    if teamAbbrev==team1:
        return "Away"
    else:
        return "Home"

def getOpponent(gameInfo,TeamAbbrev):
    team1=gameInfo[0:3]#awayteam
    team2=gameInfo[4:7]#hometeam
    if TeamAbbrev==team1:
        return team2
    else:
        return team1