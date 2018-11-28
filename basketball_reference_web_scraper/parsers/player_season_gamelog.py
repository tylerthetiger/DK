from lxml import html

from basketball_reference_web_scraper.data import Location, Outcome, TEAM_ABBREVIATIONS_TO_TEAM
def parse_player_season_row(row):

    if row[5].text_content()=="@":
        location="Away"
    else:
        location="Home"   
    opp=row[6].text_content()
    result=row[7].text_content()
    try:
        gs=int(row[8].text_content())
    except:
        gs=None #if can't get a GS, the player probably didn't play
        return None
    return {
        "rk": row[0].text_content(),
        "g": row[1].text_content(),
        "date":row[2].text_content(),
        "age":row[3].text_content(),
        "tm":row[4].text_content(),
        "location":location,
        "opp":row[6].text_content(),
        "result":row[7].text_content(),
        "gs":gs,
        "mp":row[9].text_content(),
        "fg":row[10].text_content(),
        "fga":row[11].text_content(),
        "fg%":row[12].text_content(),
        "3p":int(row[13].text_content()),
        "3pa":row[14].text_content(),
        "3p%":row[15].text_content(),
        "ft":row[16].text_content(),
        "fta":row[17].text_content(),
        "ft%":row[18].text_content(),
        "orb":row[19].text_content(),
        "drb":row[20].text_content(),
        "trb":int(row[21].text_content()),
        "ast":int(row[22].text_content()),
        "stl":int(row[23].text_content()),
        "blk":int(row[24].text_content()),
        "tov":int(row[25].text_content()),
        "pf":row[26].text_content(),
        "pts":int(row[27].text_content()),
        "GmSc":row[28].text_content(),
        "plusminus":row[29].text_content(), }
def parse_player_season(page):
    tree = html.fromstring(page)
    rows = tree.xpath('//table[@id="pgl_basic"]//tbody/tr[not(contains(@class, "thead"))]')
    game_boxscore_list = []
    for row in rows:
        retVal = parse_player_season_row(row)
        if retVal!=None:
            game_boxscore_list.append(retVal)
    return game_boxscore_list
 #   return list(map(lambda row: parse_player_season_row(row), rows))
