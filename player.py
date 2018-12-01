import datetime
import csv
from team import * 
from basketball_reference_web_scraper import client
from nba_api.stats.endpoints import commonplayerinfo, playerfantasyprofile, playergamelog
from nba_api.stats.static import players

class Player:
    def __init__(self,row):
        #name,NBAplayerID,position,avgPoints,salary,team,nextOpponent,nextGameLocation
        self.position=row[0]
        self.nameplusid=row[1]
        self.name = row[2]
        self.NBAplayerID = row[3]
        self.rosterposition = row[4]
        self.salary = row[5]
        self.gameinfo=row[6]
        self.teamabbrev=row[7]
        self.avgPoints = row[8]
        self.team = row[7] #this is the team that the player is on
        self.nextOpponent = getOpponent(row[6],self.team)
        self.lastTwoWeekAverage = 0
       # self.lastTwoWeekAverageHome = 0
       # self.lastTwoWeekAverageAway = 0

        if self.nextOpponent == "NY": #removing this - fix in data.py should be good
            self.nextOpponent = "NYK" #fix for draftkings/nba api compatibility
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
        csv_file.write("Position,Name + ID,Name,ID,Roster Position,Salary,Game Info,TeamAbbrev,AvgPointsPerGame,estimatedPoints\n")
        for player in playerObjList:
            outputString = "{},{},{},{},{},{},{},{},{},{}\n".format(player.position,player.nameplusid,player.name,player.NBAplayerID,player.rosterposition,str(player.salary),player.gameinfo,player.teamabbrev,str(player.lastTwoWeekAverage),str(player.projection))
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
    homeTeam=gameInfo[gameInfo.find("@")+1:gameInfo.find(" ")]#hometeam
    if TeamAbbrev==awayTeam:
        return homeTeam
    else:
        return awayTeam

# get data from web instead of csv
def GetInjuriesv2():
    injuries = client.injury_report()
    injuredPlayers = []

    for injuredPlayer in injuries:
        injuredPlayers.append(injuredPlayer['player'])
    
    return injuredPlayers

def GetEligiblePlayers(csvOfAllPlayers):
    allPlayers = GetListOfPlayers(csvOfAllPlayers)
    injuredPlayers = GetInjuriesv2()
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
        if playerName.lower() in boxscore['name'].lower() or boxscore['name'].lower() in playerName.lower():
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
def BasketballReferenceScoreSingleGame(boxscore):
    pointTotal=float(0)
    points=boxscore['pts']
    threepointers=boxscore['3p']
    rebounds=boxscore['trb']
    assists=boxscore['ast']
    steals=boxscore['stl']
    blocks=boxscore['blk']
    turnovers=boxscore['tov']
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
#score a game list and return the average fantasy points per game
def BasketballReferenceScoreGameList(gameList,numberOfGames,location):
    total = float(0)
    games=0
    revGames=gameList[::-1]#get most recent games!
    for game in revGames:
        if game['location']!=location:
            pass
        games+=1
        total+=BasketballReferenceScoreSingleGame(game)
        if games>=numberOfGames:
            break#stop looking at games once we've scored enough
    #if numberOfGames>games:
     #   raise Exception("Couldn't get enough games.  Needed {} got {} at location {}".format(numberOfGames,games,location))
    return float(total)/float(games) #you'll all float down here
def BasketballReferenceScorePlayer(bballrefHTML,NumberOfDays,playerObj):
    print "starting to score for player {}".format(playerObj.name)
    BASE_URL = 'https://www.basketball-reference.com'
    bballrefHTML = bballrefHTML[0:bballrefHTML.find(".")] #strip off the .html
    finalURL = BASE_URL+bballrefHTML+'/gamelog/2019'
    playerLog= client.player_season_log(finalURL)
    playerFantasyAverage = BasketballReferenceScoreGameList(playerLog,NumberOfDays,playerObj.nextGameLocation)
    playerObj.lastTwoWeekAverage = playerFantasyAverage
    print "Just scored player {} average:{}".format(playerObj.name,playerFantasyAverage)
    #player2019gamelog = BASE_URL + ''
## For every elgible player, calculate a projection, based on the last NumberOfDays
def GetProjection_bballreference(listOfPlayers,NumberOfGames=30,debugoutput=True):
                                        #we retrieve 45 days worth of data, but we'll only examine the last 14 games
    lastTwoWeeks = client.last_n_days_playerlist(45) #this is goig to return a tuple of playerName, htmlLink
    for player in listOfPlayers:
        match = None
        for l in lastTwoWeeks:
            if l[0].lower() in player.name.lower() or player.name.lower() in l[0].lower():
                match = l
                break
        if match == None:
            print("Unable to find player match for{}".format(player.name))
        else:
            BasketballReferenceScorePlayer(l[1],NumberOfGames,player)#l[1] iis the html link
            #grab the players individual season performance and score it
            #this will fill in the player.lastTwoWeekAverage 
            GetPlayerProjection(player,debugoutput=True)
           # print "found player!{}".format(player.name)
def GetPlayerProjection(player,debugoutput=True):
        lastTwoWeekAverage = projectedPoints = player.lastTwoWeekAverage#baseline projected points
        opponentTeam = player.nextOpponent
        opponentIsBackToBack = teamBacktoBack_bballreference(opponentTeam)
        if opponentIsBackToBack:
            if debugoutput:
                print 'increasing player projection due to opponent on back2back'
            projectedPoints = projectedPoints + (0.10 * lastTwoWeekAverage)
        playerIsBackToBack = BackToBack(player)
        if playerIsBackToBack:
            if debugoutput:
                print 'decreasing player projection due to back2back'
            projectedPoints = projectedPoints - (0.10 * lastTwoWeekAverage)
        print 'getting defensive ranking by player'
        teamCity = teamMapping[opponentTeam]
        # get defensive ranking by player
        defenseRanking = getPlayerDefensiveRanking()
        # print defenseRanking
        defenseOffset = defenseRanking[teamCity]
        # defenseRanking = getNextGameDefensiveRating('defensive_ranking.csv')
        # print defenseRanking
        # defenseOffset = defenseRanking[teamCity]
        if debugoutput:
            print 'adjusting player by ' + str(defenseOffset) + ' for defensive offset'
        projectedPoints = projectedPoints * defenseOffset
        
        player.projection = projectedPoints
        
# def GetInjuries (csvFileName):
#     injuredPlayers = []
#     lineCount = 0
#     with open(csvFileName) as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=',')
#         for row in csv_reader:
#             if lineCount == 0:
#                 lineCount += 1
#             else:
#                 rawName = row[0]
#                 findFullName = rawName.find("\\")
#                 nameOnly = rawName[0:findFullName]
#                 injuredPlayers.append(nameOnly)
#     return injuredPlayers

# def GetProjection(listOfPlayers,debugoutput=True,usenbaapi=False):
#     for player in listOfPlayers:
#         if debugoutput:
#             print 'getting projection for {}'.format(player.name)
#         if usenbaapi==True:
#             lastTwoWeekAverage = projectedPoints = getLastTwoWeeksAveragePoints_nbaapi(player)#baseline projected points
#         else:
#             lastTwoWeekAverage = projectedPoints = getLastTwoWeeksAveragePoints(player)#baseline projected points
#         if debugoutput:
#             print 'done getting 2 week average, getting back to back' + str(lastTwoWeekAverage)
#         playerIsBackToBack = BackToBack(player)

#         if playerIsBackToBack:
#             projectedPoints = projectedPoints - (0.10 * lastTwoWeekAverage)
#         if debugoutput:
#             print 'done getting player back to back, getting team back to back'
        
#         opponentTeam = player.nextOpponent
#         opponentIsBackToBack = teamBacktoBack_bballreference(opponentTeam)
#         if opponentIsBackToBack:
#             projectedPoints = projectedPoints + (0.10 * lastTwoWeekAverage)
#         if debugoutput:
#             print 'done getting team back to back, getting team defensive rating'
#         #TODO adjust based on team defensive ranking
#         teamCity = teamMapping[opponentTeam]
#         defenseRanking = getNextGameDefensiveRating('defensive_ranking.csv')
#         print defenseRanking
#         # print defenseRanking
#         defenseOffset = defenseRanking[teamCity]
#         projectedPoints = projectedPoints * defenseOffset
        
#         player.projection = projectedPoints

###TODO - rewrite this using https://www.basketball-reference.com/friv/last_n_days.fcgi?n=14
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
        lastName = playerName[playerName.find(" ")+1:]
        firstName = playerName[0:playerName.find(" ")] 
        for tmp_player in nba_player:
            if tmp_player['first_name'] == firstName and tmp_player['last_name']==lastName:
                playerId = tmp_player['id']
        if playerId == None:
            print "Unable to determine player id for {}".format(playerName)
            #TODO - instead of using the static nba api should do dynamic to get these players ID and get their
            return 0
    else:
        playerId = nba_player[0]['id']
    attempts=0
    while attempts<5:
        try:    
            gameLog = playergamelog.PlayerGameLog(playerId,date_from_nullable=dateToPull,date_to_nullable=today)
        except:
            print "nba api timed out, waiting 10 minutes then trying again.  Attempt {} of 5".format(attempts)
            attempts+=1
            time.sleep(600)
    if gameLog == None:
        raise Exception("NBA API still not working after 5 attempts and waiting 10 minutes, bailing")
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
    testing = getPlayerDefensiveRanking()
    print(testing)
    # pass
if __name__ == "__main__":
    main()