import requests
from bs4 import BeautifulSoup
import re
import numpy as np

#GENERAL SCRAPING FUNCTIONS

def get_page_code(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def show_more(url, offset):
    update_past_data = url + str(offset)
    update_page = get_page_code(update_past_data)
    return update_page

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    string = re.sub(clean, '', text)
    return string

def extract_parameter(tag, parameter):
    key_val = re.search(' +' + parameter + '=\"(.*?)\"', str(tag))

    value = key_val.group(1)
    return value


#KICKOFF.ai SCRAPING FUNCTIONS

def div(match):
    div_dict = {
        'fr': 'F1',
        'es': 'SP1',
        'it': 'I1',
        'de': 'D1',
        'eng': 'E0'
    }

    home_tag = match.find('div', {'class': 'team-home'})
    home_flag_tag = home_tag.find_all('span')[0]
    home_flag = extract_parameter(home_flag_tag, 'class').split('-')[-1].strip()

    away_tag = match.find('div', {'class': 'team-away'})
    away_flag_tag = away_tag.find_all('span')[1]
    away_flag = extract_parameter(away_flag_tag, 'class').split('-')[-1].strip()

    if home_flag == away_flag:
        division = div_dict[home_flag]
    else:
        division = np.nan

    return division


def team_name(match):
    home_tag = match.find('div', {'class': 'team-home'})
    home_tag = home_tag.find('span', {'class': 'team-name'})
    home_team = remove_html_tags(str(home_tag)).strip()

    away_tag = match.find('div', {'class': 'team-away'})
    away_tag = away_tag.find('span', {'class': 'team-name'})
    away_team = remove_html_tags(str(away_tag)).strip()

    return home_team, away_team


def result_match(match):
    result_tag = match.find('div', {'class': 'result'})
    result = remove_html_tags(str(result_tag))

    goal = result.split(':')

    goal_home = goal[0].strip()
    goal_away = goal[1].strip()

    if goal_home > goal_away:
        bet = 0  # WIN
    elif goal_home < goal_away:
        bet = 2  # LOSE
    else:
        bet = 1  # DRAWN

    return goal_home, goal_away, bet


def time_match(match):
    time_tag = match.find('div', {'class': 'match-time-list'})
    timestamp = remove_html_tags(str(time_tag)).strip()

    time = str(timestamp[:5])
    day = str(timestamp[6:8])
    month = str(timestamp[9:])

    import calendar

    for monthName in list(calendar.month_name):
        if month == monthName:
            month = str(list(calendar.month_name).index(monthName))

    if len(month) == 1:
        month = '0' + month

    date = day + '/' + month
    return date, time


def get_predictions(match):
    pred_tags = match.find_all('div', {'role': 'progressbar'})

    parameter = 'aria-valuenow'

    home = extract_parameter(pred_tags[0], parameter)
    drawn = extract_parameter(pred_tags[1], parameter)
    away = extract_parameter(pred_tags[2], parameter)

    return home, drawn, away
