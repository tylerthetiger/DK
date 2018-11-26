import requests

from basketball_reference_web_scraper.errors import InvalidDate
from basketball_reference_web_scraper.parsers.box_scores import parse_player_box_scores
from basketball_reference_web_scraper.parsers.schedule import parse_schedule, parse_schedule_for_month_url_paths
from basketball_reference_web_scraper.parsers.players_season_totals import parse_players_season_totals
from basketball_reference_web_scraper.parsers.injury_report import parse_injury_report
from basketball_reference_web_scraper.parsers.last_n_days import parse_last_n_days
BASE_URL = 'https://www.basketball-reference.com'


def injury_report():
    url = '{BASE_URL}/friv/injuries.fcgi'.format(BASE_URL=BASE_URL)
    response = requests.get(url=url, allow_redirects=False)
    if 200 <= response.status_code < 300:
        return parse_injury_report(response.content)
def last_n_days(days):
    url = '{BASE_URL}/friv/last_n_days.fcgi?n={DAYS}'.format(BASE_URL=BASE_URL,DAYS=days)
    response = requests.get(url=url, allow_redirects=False)
    if 200 <= response.status_code < 300:
        return parse_last_n_days(response.content)
def player_box_scores(day, month, year):
    url = '{BASE_URL}/friv/dailyleaders.cgi?month={month}&day={day}&year={year}'.format(
        BASE_URL=BASE_URL,
        day=day,
        month=month,
        year=year
    )

    response = requests.get(url=url, allow_redirects=False)

    if 200 <= response.status_code < 300:
        return parse_player_box_scores(response.content)

    raise InvalidDate(day=day, month=month, year=year)


def schedule_for_month(url):
    response = requests.get(url=url)

    response.raise_for_status()

    return parse_schedule(response.content)


def season_schedule(season_end_year):
    url = '{BASE_URL}/leagues/NBA_{season_end_year}_games.html'.format(
        BASE_URL=BASE_URL,
        season_end_year=season_end_year
    )

    response = requests.get(url=url)

    response.raise_for_status()

    season_schedule_values = parse_schedule(response.content)
    other_month_url_paths = parse_schedule_for_month_url_paths(response.content)

    for month_url_path in other_month_url_paths:
        url = '{BASE_URL}{month_url_path}'.format(BASE_URL=BASE_URL, month_url_path=month_url_path)
        monthly_schedule = schedule_for_month(url=url)
        season_schedule_values.extend(monthly_schedule)

    return season_schedule_values


def players_season_totals(season_end_year):
    url = '{BASE_URL}/leagues/NBA_{season_end_year}_totals.html'.format(
        BASE_URL=BASE_URL,
        season_end_year=season_end_year,
    )

    response = requests.get(url=url)

    response.raise_for_status()

    return parse_players_season_totals(response.content)
