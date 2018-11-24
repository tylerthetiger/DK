from pydfs_lineup_optimizer import get_optimizer, Site, Sport
import datetime
from nba_api.stats.endpoints import commonplayerinfo, playerfantasyprofile,playergamelog
from nba_api.stats.static import players
from basketball_reference_web_scraper import client
from player import writePlayerProjectsionToCSV, FantasyScoreFromSingleGame, GetEligiblePlayers,GetProjection
today=datetime.datetime.today().strftime('%m/%d/%Y')
yesterday=(datetime.datetime.now() - datetime.timedelta(1)).strftime('%m/%d/%Y')


def GetOptimizedLineup(csvFileName):
    optimizer = get_optimizer(Site.DRAFTKINGS,Sport.BASKETBALL)
    optimizer.load_players_from_csv(csvFileName)
    lineups = optimizer.optimize(n=1)
    for lineup in lineups:
        print lineup
def main():
    #getLastTwoWeeksAveragePoints("Dennis Schroder")
    eligibleList = GetEligiblePlayers('DKSalaries-Contest1.csv', 'injuries.csv')
    print 'finished getting list of eligible players ({} players)'.format(str(len(eligibleList)))
    print 'getting player projections'
    GetProjection(eligibleList,debugoutput=True)
    print 'finished getting projections'
    writePlayerProjectsionToCSV('DKSalaries-projected.csv',eligibleList)
    print 'finished writing out projections to csv'
    print 'getting optimized lineup'
    GetOptimizedLineup('DKSalaries-projected.csv')

    return None
if __name__=="__main__":
    main()