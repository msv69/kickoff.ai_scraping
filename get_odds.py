import requests
import zipfile
import io
import pandas as pd
import os

seasonList = {
    '2017/2018': 'http://www.football-data.co.uk/mmz4281/1718/data.zip',
    '2018/2018': 'http://www.football-data.co.uk/mmz4281/1819/data.zip'
}

fileList = [
    'E0.csv',
    'I1.csv',
    'G1.csv',
    'F1.csv',
    'SP1.csv'
]

cols = ['Div', 'Date', 'HomeTeam', 'AwayTeam',
        'B365H', 'B365D', 'B365A']


def add_odds(df):

    odds = pd.DataFrame(columns=cols)

    for season in list(seasonList.values()):
        r = requests.get(season)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall()

        for fileName in z.namelist():
            if fileName in fileList:

                file = pd.read_csv(fileName)
                file = file[file.columns.intersection(cols)]

                for i, date in enumerate(file['Date']):
                    date = (date.split('/')[0] + '/' + date.split('/')[1]).strip()
                    file.loc[i, 'Date'] = date

                odds = odds.append(file, ignore_index=True)


    # SOLVE PROBLEM DIFFERENT NAME OF TEAMS

    df = pd.merge(df, odds, on=['HomeTeam', 'AwayTeam', 'Date'])
    # df_2 = pd.merge(df, odds, on=['Div', 'AwayTeam', 'Date'])
    # df = pd.concat([df_1, df_2], ignore_index=True, sort=True).drop_duplicates().reset_index(drop=True)

    for fileName in z.namelist():
        os.remove(fileName)

    return df







