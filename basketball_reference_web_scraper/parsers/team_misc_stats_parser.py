from lxml import html

from basketball_reference_web_scraper.data import TEAM_ABBREVIATIONS_TO_TEAM, POSITION_ABBREVIATIONS_TO_POSITION

def parse_team_misc_stats(row):
  #  print row
    if row[13].text_content() == " " or row[13].text_content() == "":
        pace = 0
    else:
        pace = float(row[13].text_content())

	return {
        "team_name": str(row[1].text_content()),
		"pace": pace,
	}

def parse_teams_misc_stats(page):
    page = page[page.find("<table class=\"sortable stats_table\" id=\"misc_stats\" data-cols-to-freeze=2><caption>Miscellaneous Stats Table</caption>"):]
    page = page[0:page.find("</table>")+len("</table>")]
    tree = html.fromstring(page)
    # Basketball Reference includes individual rows for players that played for multiple teams in a season
    # These rows have a separate class ("italic_text partial_table") than the players that played for a single team
    # across a season.
    # no class on rows in this dataset

    rows = tree.xpath('//table[@id="misc_stats"]/tbody/tr ')
    totals = []
    for row in rows:
        # Basketball Reference includes a "total" row for players that got traded
        # which is essentially a sum of all player team rows
        # I want to avoid including those, so I check the "team" field value for "TOT"
        if row[4].text_content() != "TOT":
            totals.append(parse_team_misc_stats(row))
        # totals.append(parse_player_100_poss(row))
    return totals