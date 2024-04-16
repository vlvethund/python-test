import requests
import json
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, Date, Float, Text, DECIMAL
from sqlalchemy.orm import sessionmaker
from store.stockpricehistoricaldataentity import StockPriceHistoricalData
from dotenv import load_dotenv
import os
from pytz import timezone


load_dotenv()
dburl = os.environ.get('dburl')
tz = timezone('America/New_York')

symbol = 'AAPL'
start = '2000-01-01'
end = 'today'


stock_price_historical_data_table = Table(
    'stock_price_historical_data', MetaData(),
    Column('symbol', Text, primary_key=True),
    Column('date', Date, primary_key=True),
    Column('open', Float),
    Column('high', Float),
    Column('low', Float),
    Column('close', Float),
    Column('adj_close', Float),
    Column('volume', DECIMAL),
)

insertArr = []

startSplit = start.split('-')

startDateTime = datetime(int(startSplit[0]), int(startSplit[1]), int(startSplit[2]), 0, 0, 0, tzinfo=tz)
endDateTime = datetime.today().astimezone(tz)


if end != 'today':
    endSplit = end.split('-')
    endDateTime = datetime(int(endSplit[0]), int(endSplit[1]), int(endSplit[2]), 0, 0, 0, tzinfo=tz)

startUnix = int(startDateTime.timestamp())
endUnix = int(endDateTime.timestamp())

url = f'https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?formatted=true&crumb=BAeTUdnAlvz&lang=en-US&region=US&includeAdjustedClose=true&interval=1d&period1={startUnix}&period2={endUnix}&events=capitalGain%7Cdiv%7Csplit&useYfid=true&corsDomain=finance.yahoo.com'

response = requests.get(url, headers={'user-agent': 'sdfsdf', 'Accept': 'application/json, text/plain, */*'})

if response.status_code == 200:
    content = response.content.decode('utf-8')
    body = json.loads(content)

    for idx, unix_time in enumerate(body['chart']['result'][0]['timestamp']):
        date = datetime.utcfromtimestamp(unix_time).astimezone(tz)
        open = body['chart']['result'][0]['indicators']['quote'][0]['open'][idx]
        high = body['chart']['result'][0]['indicators']['quote'][0]['high'][idx]
        low = body['chart']['result'][0]['indicators']['quote'][0]['low'][idx]
        close = body['chart']['result'][0]['indicators']['quote'][0]['close'][idx]
        volume = body['chart']['result'][0]['indicators']['quote'][0]['volume'][idx]
        adjclose = body['chart']['result'][0]['indicators']['adjclose'][0]['adjclose'][idx]

        obj = {'symbol': symbol, 'date': date, 'open': open, 'high': high, 'low': low, 'close': close,
               'adjclose': adjclose}

        insertArr.append(StockPriceHistoricalData(symbol=symbol, date=date, open=open, high=high, low=low, close=close, adj_close=adjclose))


engine = create_engine(f'mysql+pymysql://{dburl}')


Session = sessionmaker()
Session.configure(bind=engine)

session = Session()
# session.add_all(insertArr)
# session.commit()

