from lxml import html

from basketball_reference_web_scraper.data import Location, Outcome, TEAM_ABBREVIATIONS_TO_TEAM

def parse_injury_report_row(row):
    return {
        "player": row[0].text_content(),
        "team": row[1].text_content(),
        "date":row[2].text_content(),
        "description":row[3].text_content(),
    }
def parse_injury_report(page):
    tree = html.fromstring(page)
    rows = tree.xpath('//table[@id="injuries"]//tbody/tr[not(contains(@class, "thead"))]')
    return list(map(lambda row: parse_injury_report_row(row), rows))
