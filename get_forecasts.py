import scraping as s
import pandas as pd

cols = [
    'Div',
    'Date',
    'Time',
    'HomeTeam',
    'AwayTeam',
    'oddsHome',
    'oddsDrawn',
    'oddsAway',
    'GoalHome',
    'GoalAway',
    'Result'
]

past_data = 'https://kickoff.ai/more-matches?which=results&offset='
new_forecast = 'https://kickoff.ai/more-matches?which=fixtures&offset='


def get_past_data(past_data=past_data):
    df_past = pd.DataFrame(columns=cols)

    offset = 0

    update_page = s.show_more(past_data, offset)
    match = update_page.find('div', {'class': 'prediction prediction-result'})

    while str(match) != 'None':
        new_match = dict()

        # append league
        new_match[cols[0]] = s.div(match)

        # append date
        date, time = s.time_match(match)

        new_match[cols[1]] = date
        new_match[cols[2]] = time

        # append teams
        home_team, away_team = s.team_name(match)

        new_match[cols[3]] = home_team
        new_match[cols[4]] = away_team

        # append odds
        home, drawn, away = s.get_predictions(match)

        new_match[cols[5]] = home
        new_match[cols[6]] = drawn
        new_match[cols[7]] = away

        # append result
        goal_home, goal_away, bet = s.result_match(match)

        new_match[cols[8]] = goal_home
        new_match[cols[9]] = goal_away
        new_match[cols[10]] = bet

        # add new match to df
        df_past = df_past.append(new_match, ignore_index=True)

        offset += 1

        if offset % 50 == 0:
            print('Loading........................{}'.format(offset))

        update_page = s.show_more(past_data, offset)
        match = update_page.find('div', {'class': 'prediction prediction-result'})

    return df_past


def get_new_forecast(new_forecast=new_forecast):
    df_new = pd.DataFrame(columns=cols)

    offset = 0

    update_page = s.show_more(new_forecast, offset)
    match = update_page.find('div', {'class': 'prediction prediction-fixture'})

    while str(match) != 'None':
        new_match = dict()

        # append league
        new_match[cols[0]] = s.div(match)

        # append date
        date, time = s.time_match(match)

        new_match[cols[1]] = date
        new_match[cols[2]] = time

        # append teams
        home_team, away_team = s.team_name(match)

        new_match[cols[3]] = home_team
        new_match[cols[4]] = away_team

        # append odds
        home, drawn, away = s.get_predictions(match)

        new_match[cols[5]] = home
        new_match[cols[6]] = drawn
        new_match[cols[7]] = away

        # append result
        goal_home, goal_away, bet = s.result_match(match)

        new_match[cols[8]] = goal_home
        new_match[cols[9]] = goal_away
        new_match[cols[10]] = bet

        # add new match to df
        df_new = df_new.append(new_match, ignore_index=True)

        offset += 1

        update_page = s.show_more(new_forecast, offset)
        match = update_page.find('div', {'class': 'prediction prediction-fixture'})

    return df_new


