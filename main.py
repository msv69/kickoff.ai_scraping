from get_forecasts import get_past_data
from get_odds import add_odds
import pandas as pd

if __name__ == "__main__":
    #df_past = get_past_data()
    #df_past.to_csv('/Users/eliogruttadauria/Desktop/df_past.csv', index=False)

    df_past = pd.read_csv('/Users/eliogruttadauria/Desktop/df_past.csv')

    df_past = add_odds(df_past)
    df_past.to_csv('/Users/eliogruttadauria/Desktop/df_pastOdds.csv', index=False)

    #df_new = get_new_forecast()
    #df_new.to_csv('/Users/eliogruttadauria/Desktop/df_new.csv')
