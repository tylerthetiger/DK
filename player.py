import datetime
import csv
from basketball_reference_web_scraper import client
from nba_api.stats.endpoints import commonplayerinfo, playerfantasyprofile,playergamelog
from nba_api.stats.static import players

class Player:
    def __init__(self,row):
        #name,NBAplayerID,position,avgPoints,salary,team,nextOpponent,nextGameLocation
        self.position=row[0]
        self.nameplusid=row[1]
        # account for misspelled names
        self.name = row[2]
        #if self.name == 'Juancho Hernangomez':
        #    self.name = 'Juan Hernangomez'
        
        self.NBAplayerID = row[3]
        self.rosterposition = row[4]
        self.salary = row[5]
        self.gameinfo=row[6]
        self.teamabbrev=row[7]
        self.avgPoints = row[8]
        self.team = row[7] #this is the team that the player is on
        self.nextOpponent = getOpponent(row[6],self.team)
        self.nextGameLocation = getLocation(row[6],self.team)#should be home or away
        self.projection = 0
    def __repr__(self):
        return 'Player({},{},{},{},{},{},{},{},{})'.format(self.name,self.NBAplayerID,self.position,self.avgPoints,self.salary,self.team,self.nextOpponent,self.nextGameLocation,self.projection)
       # return (self.name + ', ' + self.position + ', ' + self.avgPoints + ', ' + self.salary)
    def __str__(self):
        return '{},{},{},{},{},{},{},{},{}'.format(self.name,self.NBAplayerID,self.position,self.avgPoints,self.salary,self.team,self.nextOpponent,self.nextGameLocation,self.projection)

        #return (self.name + ', ' + self.position + ', ' + self.avgPoints + ', ' + self.salary)

def writePlayerProjectsionToCSV(csvFileName,playerObjList):
    with open(csvFileName,'w') as csv_file:
        csv_file.write("Position,Name + ID,Name,ID,Roster Position,Salary,Game Info,TeamAbbrev,AvgPointsPerGame\n")
        for player in playerObjList:
            outputString = "{},{},{},{},{},{},{},{},{}\n".format(player.position,player.nameplusid,player.name,player.NBAplayerID,player.rosterposition,str(player.salary),player.gameinfo,player.teamabbrev,str(player.projection))
            csv_file.write(outputString)

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
def GetEligiblePlayers(csvOfAllPlayers, csvOfInjuredPlayers):
    allPlayers = GetListOfPlayers(csvOfAllPlayers)
    injuredPlayers = GetInjuries(csvOfInjuredPlayers)
    eligiblePlayers = []
    finalList = []

    for player in allPlayers:
        eligiblePlayers.append(player)

    for eligible in eligiblePlayers:
        playerIsInjured=False
        for injured in injuredPlayers:
            if injured in eligible.name:
                playerIsInjured=True
          
        if playerIsInjured==False:
            finalList.append(eligible)

    return finalList

def getBoxScoreForPlayerFromLists(playerName,BoxScoreList):
    for boxscore in BoxScoreList:
        #print boxscore['name']
        #print playerName
        if playerName.lower() in boxscore['name'].lower() or playerName.lower() in boxscore['name'].lower():
            return boxscore
    return None
def FantasyScoreFromSingleGame(boxscore):
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

## IN: NBAPlayerID
## Return: True if today's game will be a back-to-back, false otherwise
def BackToBack(playerObj):
    playerName = playerObj.name
    dateToPull=(datetime.datetime.now() - datetime.timedelta(1))
    yesterdayGames = client.player_box_scores(day=dateToPull.day, month=dateToPull.month, year=dateToPull.year)
    for boxscore in yesterdayGames:
        if boxscore['name'] in playerName or playerName in boxscore['name']:
            return True
    return False

# get list of injured players from https://www.basketball-reference.com/friv/injuries.fcgi
# returns a list of names of players that are injured
def GetInjuries (csvFileName):
    injuredPlayers = []
    lineCount = 0
    with open(csvFileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if lineCount == 0:
                lineCount += 1
            else:
                rawName = row[0]
                findFullName = rawName.find("\\")
                nameOnly = rawName[0:findFullName]
                injuredPlayers.append(nameOnly)
    return injuredPlayers

def GetProjection(listOfPlayers,debugoutput=False):
    for player in listOfPlayers:
        if debugoutput:
            print 'getting projection for {}'.format(player.name)
        lastTwoWeekAverage = projectedPoints = getLastTwoWeeksAveragePoints_nbaapi(player)#baseline projected points
        playerIsBackToBack = BackToBack(player)
        if playerIsBackToBack:
            projectedPoints = projectedPoints - 0.01*projectedPoints  #1% decrease if playing in a back to back
        ##todo, give a boost if the opponent is coming off of a back to back
        player.projection = projectedPoints


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
def getFantasyPointsFromDF(df):
    pointTotal = float(0)
    for i in range(0,len(df)):
        points=df['PTS'][i]
        threepointers=df['FG3M'][i]
        rebounds=df['REB'][i]
        assists=df['AST'][i]
        steals=df['STL'][i]
        blocks=df['BLK'][i]
        turnovers=df['TOV'][i]
        numberDoubleCategories=0
        if points>=10:
            numberDoubleCategories+=1
        if rebounds>=10:
            numberDoubleCategories+=1
        if assists>=10:
            numberDoubleCategories+=1
        if blocks>=10:
            numberDoubleCategories+=1
        if steals>=10:
            numberDoubleCategories+=1
        if numberDoubleCategories>=2:
            pointTotal+=1.5
        if numberDoubleCategories>=3:
            pointTotal+=3
        pointTotal+=points
        pointTotal+=(threepointers*0.5)
        pointTotal+=(rebounds*1.25)
        pointTotal+=(assists*1.5)
        pointTotal+=(steals*2)
        pointTotal+=(blocks*2)
        pointTotal+=(turnovers*-0.5)


    return pointTotal
###TESTING### TODO fix this...matching John Wallace for John Wall. 
def getLastTwoWeeksAveragePoints_nbaapi(playerObj):
    playerName = playerObj.name
    dateIndex = 1 #counter to keep track of how many days back we are going
    totalGamesPlayed=0
    totalFantasyPoints=0
    today=datetime.datetime.today().strftime('%m/%d/%Y')
    dateToPull=(datetime.datetime.now() - datetime.timedelta(14)).strftime('%m/%d/%Y')

    nba_player = players.find_players_by_full_name(playerName)
    playerId=None
    if len(nba_player)!=1:
        print 'len(nba_player) is {} for player: {}'.format(str(len(nba_player)),playerName)
        for a in nba_player:
            print a['full_name']
            print a['id']
        raise Exception("Bailing")
    else:
        playerId = nba_player[0]['id']
    gameLog = playergamelog.PlayerGameLog(playerId,date_from_nullable=dateToPull,date_to_nullable=today)
    gameLogDf=gameLog.get_data_frames()[0]
    totalFantasyPoints = getFantasyPointsFromDF(gameLogDf)
    if len(gameLogDf)==0:
        print "{} played 0 games!".format(playerName)
        return 0
    return totalFantasyPoints/len(gameLogDf)
    

def GetListOfPlayers(csvFileName):
    listOfPlayers = []
    lineCount=0
    with open(csvFileName) as csv_file:
       csv_reader = csv.reader(csv_file, delimiter=',')
       for row in csv_reader:
            if lineCount == 0:
                lineCount+=1 #skip the header
            else:
                #TODO addd the actual nba player id not the draft kings ID
                tempPlayerObj=Player(row)
                listOfPlayers.append(tempPlayerObj)
    return listOfPlayers

def main():
    pass
if __name__ == "__main__":
    main()