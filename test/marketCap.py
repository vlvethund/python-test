import sys

sys.path.append('.')

import json

import requests
from datetime import datetime
from pytz import timezone
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, cast, DATE
from sqlalchemy.orm import sessionmaker
from store.marketcaphistocialdata import MarketCapHistoricalData
from module.getHistoricalData import get_historical_data

tz = timezone('America/New_York')
load_dotenv()
dburl = os.environ.get('dburl')

params2 = {
    'crumb': 'WFUUfvdDToA',
    'formatted': 'true'
}

headers2 = {
    'Cookie': 'axids=gam=y-Pkq14dtE2uJJK4bZFjz7ZgWv.w.CXYar~A&dv360=eS0xUnp5SS5WRTJ1R1Z1VldPamt6dWxXYm5UWUs2Y2tNb35B&ydsp=y-lIq6EctE2uI5CjVLu80uFBMLAOxJC8Jz~A&tbla=y-bTJc.o9E2uIN_5RcT5oezEMbkWAXICce~A; tbla_id=485cdde1-664c-4ff0-b679-e784b56e8698-tuct9c00962; GUC=AQEBCAFmENlmPkIa9gQN&s=AQAAAMI9yvd0&g=Zg-TgA; A1=d=AQABBPKYxmICEP6o1TfN9QwGVFLyzmwoxHEFEgEBCAHZEGY-Zmdkb2UB_eMBAAcI8pjGYmwoxHE&S=AQAAAiYrej3Yf-rUHYu4glyh3WU; A3=d=AQABBPKYxmICEP6o1TfN9QwGVFLyzmwoxHEFEgEBCAHZEGY-Zmdkb2UB_eMBAAcI8pjGYmwoxHE&S=AQAAAiYrej3Yf-rUHYu4glyh3WU; PRF=t%3D%255EIXIC%252BGE%252BXOM%252BGOOG%252BAAPL%252BCANQ%26newChartbetateaser%3D1; A1S=d=AQABBPKYxmICEP6o1TfN9QwGVFLyzmwoxHEFEgEBCAHZEGY-Zmdkb2UB_eMBAAcI8pjGYmwoxHE&S=AQAAAiYrej3Yf-rUHYu4glyh3WU; cmp=t=1712905314&j=0&u=1---; gpp=DBAA; gpp_sid=-1',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, utf-8, zstd',
    'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.0.3705;)',
    'X-Requested-With': 'XMLHttpRequest'
}

data2 = {"size": 25, "offset": 0, "sortField": "intradaymarketcap", "sortType": "DESC", "quoteType": "EQUITY",
         "topOperator": "AND", "query": {"operator": "AND", "operands": [
        {"operator": "or", "operands": [{"operator": "EQ", "operands": ["region", "us"]}]},
        {"operator": "or", "operands": [{"operator": "GT", "operands": ["intradaymarketcap", 100000000000]}]}]},
         "userId": "", "userIdType": "guid"}

res2 = requests.post('https://query2.finance.yahoo.com/v1/finance/screener', headers=headers2, data=json.dumps(data2),
                     params=params2)

if res2.status_code == 200:
    body = res2.json().get('finance').get('result')[0].get('quotes')
    engine = create_engine(f'mysql+pymysql://{dburl}')

    Session = sessionmaker()
    Session.configure(bind=engine)

    session = Session()

    for item in body:

        symbol = item.get('symbol')
        marketUnixTime = item.get('regularMarketTime').get('raw')
        marketTime = datetime.fromtimestamp(marketUnixTime, tz)
        marketCap = item.get('marketCap').get('raw')

        print('symbol: ', symbol)
        print('marketUnixTime: ', marketUnixTime)
        print('marketTime: ', marketTime)
        print('marketCap: ', marketCap)
        print('-------------------------------------------------------')

        exists = (session.query(MarketCapHistoricalData)
                  .filter(MarketCapHistoricalData.symbol == symbol)
                  .filter(cast(MarketCapHistoricalData.date, DATE) == marketTime.date())
                  .all())

        if len(exists) <= 0:
            session.add(MarketCapHistoricalData(symbol=symbol, date=marketTime, market_cap=marketCap))
            get_historical_data(symbol, marketTime.strftime('%Y-%m-%d'), marketTime.strftime('%Y-%m-%d'))

    session.commit()
