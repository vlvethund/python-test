import requests
import json
from datetime import datetime
import time
from sqlalchemy import create_engine, MetaData, Table, Column, Date, Double, Text, DECIMAL
from sqlalchemy.orm import sessionmaker
from store.stockpricehistoricaldata import stock_price_historical_data
from dotenv import load_dotenv
import os

load_dotenv()
dburl = os.environ.get('dburl')

symbol = 'AAPL'
start = '2024-03-01'
end = 'today'

stock_price_historical_data_table = Table(
    'stock_price_historical_data', MetaData(),
    Column('symbol', Text, primary_key=True),
    Column('date', Date, primary_key=True),
    Column('open', Double),
    Column('high', Double),
    Column('low', Double),
    Column('close', Double),
    Column('adj_close', Double),
    Column('volume', DECIMAL),
)

insertArr = []

startDateTime = datetime.strptime(start, '%Y-%m-%d')
endDateTime = datetime.today()
if end != 'today':
    endDateTime = datetime.strptime(end, '%Y-%m-%d')

startUnix = int(time.mktime(startDateTime.timetuple()))
endUnix = int(time.mktime(endDateTime.timetuple()))

url = f'https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?formatted=true&crumb=BAeTUdnAlvz&lang=en-US&region=US&includeAdjustedClose=true&interval=1d&period1={startUnix}&period2={endUnix}&events=capitalGain%7Cdiv%7Csplit&useYfid=true&corsDomain=finance.yahoo.com'

response = requests.get(url, headers={'user-agent': 'sdfsdf', 'Accept': 'application/json, text/plain, */*'})

if response.status_code == 200:
    content = response.content.decode('utf-8')
    body = json.loads(content)

    for idx, unix_time in enumerate(body['chart']['result'][0]['timestamp']):
        date = datetime.utcfromtimestamp(unix_time)
        open = body['chart']['result'][0]['indicators']['quote'][0]['open'][idx]
        high = body['chart']['result'][0]['indicators']['quote'][0]['high'][idx]
        low = body['chart']['result'][0]['indicators']['quote'][0]['low'][idx]
        close = body['chart']['result'][0]['indicators']['quote'][0]['close'][idx]
        adjclose = body['chart']['result'][0]['indicators']['adjclose'][0]['adjclose'][idx]

        obj = {'symbol': symbol, 'date': date, 'open': open, 'high': high, 'low': low, 'close': close,
               'adjclose': adjclose}

        insertArr.append(stock_price_historical_data(symbol=symbol, date= date, open=open, high=high, low=low, close=close, adj_close=adjclose))


engine = create_engine(
    f'mysql+pymysql://{dburl}')

Session = sessionmaker()
Session.configure(bind=engine)

session = Session()
session.add_all(insertArr)
session.commit()

# query = stock_price_historical_data_table.insert(insertArr)
# conn = engine.connect()
# conn.execute(query)
