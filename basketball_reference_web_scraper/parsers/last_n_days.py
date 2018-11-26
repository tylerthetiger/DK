from lxml import html

from basketball_reference_web_scraper.data import Location, Outcome, TEAM_ABBREVIATIONS_TO_TEAM
def parse_last_n_days_row(row):
#Rk	Player	Tm	G	GS	MP	FG	FGA	FG%	3P	3PA	3P%	FT	FTA	FT%	ORB	DRB	TRB	AST	STL	BLK	TOV	PF	PTS	GmSc
    return {
        "rank": row[0].text_content(),
        "playerName": row[1].text_content(),
        "team":row[2].text_content(),
        "games":row[3].text_content(),
        "gamesStarted": row[4].text_content(),
        "minutesPlayed": row[5].text_content(),
        "FG":row[6].text_content(),
        "FGA":row[7].text_content(),

        "FG_PERCENTAGE": row[8].text_content(),
        "3P": row[9].text_content(),
        "3PA":row[10].text_content(),
        "3P_PERCENTAGE":row[11].text_content(),

        "FT": row[12].text_content(),
        "FTA": row[13].text_content(),
        "FT_PERCENTAGE":row[14].text_content(),
        "ORB":row[15].text_content(),
    
        "DRB": row[16].text_content(),
        "TRB": row[17].text_content(),
        "AST":row[18].text_content(),
        "STL":row[19].text_content(),
        
        "BLK": row[20].text_content(),
        "TOV": row[21].text_content(),
        "PF":row[22].text_content(),
        "PTS":row[23].text_content(),
        
    }
def parse_last_n_days(page):
    tree = html.fromstring(page)
    rows = tree.xpath('//table[@id="players"]//tbody/tr[not(contains(@class, "thead"))]')
    return list(map(lambda row: parse_last_n_days_row(row), rows))