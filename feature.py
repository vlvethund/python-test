import requests
from pytz import timezone
from datetime import datetime
from store.stockpricehistoricaldata import stock_price_historical_data


tz = timezone('EST')


def get_data(symb, start, end):
    start_unix = int(start.timestamp())
    end_unix = int(end.timestamp())

    url = f'https://query2.finance.yahoo.com/v8/finance/chart/{symb}?formatted=true&crumb=BAeTUdnAlvz&lang=en-US&region=US&includeAdjustedClose=true&interval=1d&period1={start_unix}&period2={end_unix}&events=capitalGain%7Cdiv%7Csplit&useYfid=true&corsDomain=finance.yahoo.com'
    return requests.get(url, headers={'user-agent': 'sdfsdf', 'Accept': 'application/json, text/plain, */*'})

def save_data(content, sqlalchemy_session):
    insert_arr = []

    symbol = content['chart']['result'][0]['meta']['symbol']

    for idx, unix_time in enumerate(content['chart']['result'][0]['timestamp']):
        date = datetime.utcfromtimestamp(unix_time).astimezone(tz)
        open = content['chart']['result'][0]['indicators']['quote'][0]['open'][idx]
        high = content['chart']['result'][0]['indicators']['quote'][0]['high'][idx]
        low = content['chart']['result'][0]['indicators']['quote'][0]['low'][idx]
        close = content['chart']['result'][0]['indicators']['quote'][0]['close'][idx]
        volume = content['chart']['result'][0]['indicators']['quote'][0]['volume'][idx]
        adjclose = content['chart']['result'][0]['indicators']['adjclose'][0]['adjclose'][idx]

        insert_arr.append(stock_price_historical_data(symbol=symbol, date= date, open=open, high=high, low=low,
                                                      close=close, adj_close=adjclose, volume=volume))

    sqlalchemy_session.add_all(insert_arr)
    sqlalchemy_session.commit()