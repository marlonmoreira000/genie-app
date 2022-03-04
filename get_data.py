from multiprocessing.dummy import current_process
import requests
import pandas as pd
import time
from datetime import datetime

def get_weekly_eth_data():
    """
    Gets ethereum price data for the past week from Coingecko API.
    """
    BASE_URL = "https://api.coingecko.com/api/v3"
    ENDPOINT = "/coins/ethereum/market_chart/range"
    TIME_PERIOD_DAYS = 7
    DATE_CURRENT = int(time.time())
    DATE_FROM = DATE_CURRENT - (TIME_PERIOD_DAYS * 24 * 60 * 60)
    api_url = f"{BASE_URL}{ENDPOINT}"
    parameters = {
        "vs_currency": "usd",
        "from": f"{DATE_FROM}",
        "to": f"{DATE_CURRENT}"
    }

    # get the response
    response = requests.get(api_url, params=parameters).json()
    # get the list inside the response
    prices = response['prices']

    # take only the comment strings out of the response
    prices_list = []
    dates_list = []
    for price in prices:
        dates_list.append(price[0])
        prices_list.append(price[1])

    def return_first_10(x):
        """ return the first 10 digits of a number """
        return int(str(x)[:-3])
    def change_unix_timestamp_to_str(ts):
        """ change a unix timestamp into an english string """
        return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    dates = pd.Series(dates_list)
    prices = pd.Series(prices_list)
    data = pd.DataFrame({"datetime": dates, "eth_price_usd": prices})
    data["datetime"] = data["datetime"].map(return_first_10)
    data["datetime"] = data["datetime"].map(change_unix_timestamp_to_str)

    return data

def get_current_price():
    """
    Gets current ethereum price in usd from Coingecko API.
    """
    BASE_URL = "https://api.coingecko.com/api/v3"
    ENDPOINT = "/simple/price"
    api_url = f"{BASE_URL}{ENDPOINT}"
    parameters = {
        "ids": "ethereum",
        "vs_currencies": "usd",
        "include_market_cap": "false",
        "include_24hr_vol": "false",
        "include_24hr_change": "false",
        "include_last_updated_at": "false"
    }
    response = requests.get(api_url, params=parameters).json()
    current_price = round(response["ethereum"]["usd"])

    return current_price

if __name__ == "__main__":
    print(get_current_price())
