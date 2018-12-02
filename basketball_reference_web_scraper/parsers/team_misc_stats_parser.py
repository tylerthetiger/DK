from lxml import html

from basketball_reference_web_scraper.data import TEAM_ABBREVIATIONS_TO_TEAM, POSITION_ABBREVIATIONS_TO_POSITION

def parse_team_misc_stats(row):
	return {
		"pace": str(row[12].text_content()),
	}

def parse_teams_misc_stats(page):
    tree = html.fromstring(page)
    # Basketball Reference includes individual rows for players that played for multiple teams in a season
    # These rows have a separate class ("italic_text partial_table") than the players that played for a single team
    # across a season.
    # no class on rows in this dataset
    rows = tree.xpath('//table[@id="misc_stats"]/tbody/tr ')
    print(rows)
    totals = []
    for row in rows:
    	print(row)
        # Basketball Reference includes a "total" row for players that got traded
        # which is essentially a sum of all player team rows
        # I want to avoid including those, so I check the "team" field value for "TOT"
        if row[4].text_content() != "TOT":
            totals.append(parse_team_misc_stats(row))
        # totals.append(parse_player_100_poss(row))
    print('checking parser')
    print(totals)
    return totals