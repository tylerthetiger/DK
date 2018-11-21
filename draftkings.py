from pydfs_lineup_optimizer import get_optimizer, Site, Sport
optimizer = get_optimizer(Site.DRAFTKINGS,Sport.BASKETBALL)
optimizer.load_players_from_csv('./DKSalaries.csv')
lineups = optimizer.optimize(n=1)
for lineup in lineups:
    print lineup
 #   print lineup.players
 #   print lineup.fantasy_points_projection
   # print lineup.salary_costs
