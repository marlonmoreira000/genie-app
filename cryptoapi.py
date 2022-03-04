import requests
from datetime import datetime
import pandas as pd

def get_prediction():
    """ returns a prediction of Ethereum price change (%) for tomorrow """
    # set up api parameters
    BASE_URL = 'https://api-finished-3-5qxlaqr3uq-de.a.run.app'
    ENDPOINT = '/predict'
    url = f"{BASE_URL}{ENDPOINT}"
    # get response
    response = requests.get(url).json()
    prediction = response['Prediction']

    return prediction


def get_backtest(amount_usd, deposit_date):
    """ returns a df of the backtest performance using our strategy """
    # set up api parameters
    BASE_URL = 'https://api-finished-3-5qxlaqr3uq-de.a.run.app'
    ENDPOINT = '/backtest'
    url = f"{BASE_URL}{ENDPOINT}"
    today_date = datetime.today().strftime('%Y-%m-%d')
    full_url = f"https://api-finished-3-5qxlaqr3uq-de.a.run.app/backtest?amount={amount_usd}&from_date={deposit_date}&to_date={today_date}"
    response = requests.get(full_url).json()
    df = pd.DataFrame({
        'date': response['date'],
        'buy-and-hold': response['close'],
        'strategy': response['strategy']
    })

    return df

if __name__ == "__main__":
    print(get_prediction())
