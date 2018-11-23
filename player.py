class Player:
    def __init__(self,row):
        #name,NBAplayerID,position,avgPoints,salary,team,nextOpponent,nextGameLocation
        self.name = row[2]
        self.NBAplayerID = row[3]
        self.position = row[4]
        self.avgPoints = row[8]
        self.salary = row[5]
        self.team = row[7] #this is the team that the player is on
        self.nextOpponent = getOpponent(row[6],self.team)
        self.nextGameLocation = getLocation(row[6],self.team)#should be home or away
        self.projection = 0
    def __repr__(self):
        return 'Player({},{},{},{},{},{},{},{})'.format(self.name,self.NBAplayerID,self.position,self.avgPoints,self.salary,self.team,self.nextOpponent,self.nextGameLocation,self.projection)
       # return (self.name + ', ' + self.position + ', ' + self.avgPoints + ', ' + self.salary)
    def __str__(self):
        return '{},{},{},{},{},{},{},{}'.format(self.name,self.NBAplayerID,self.position,self.avgPoints,self.salary,self.team,self.nextOpponent,self.nextGameLocation,self.projection)

        #return (self.name + ', ' + self.position + ', ' + self.avgPoints + ', ' + self.salary)
    
def getLocation(gameInfo,teamAbbrev):
    awayTeam=gameInfo[0:gameInfo.find("@")]#awayteam
    homeTeam=gameInfo[gameInfo.find("@")+1:]#hometeam
    if teamAbbrev==awayTeam:
        return "Away"
    else:
        return "Home"

def getOpponent(gameInfo,TeamAbbrev):
    #gameinfo example = GS@POR
    awayTeam=gameInfo[0:gameInfo.find("@")]#awayteam
    homeTeam=gameInfo[gameInfo.find("@")+1:]#hometeam
    if TeamAbbrev==awayTeam:
        return homeTeam
    else:
        return awayTeam