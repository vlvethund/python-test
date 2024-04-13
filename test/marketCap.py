
import sys
sys.path.append('.')

import json

import requests
from datetime import datetime
from pytz import timezone
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from store.marketcaphistocialdata import MarketCapHistoricalData


tz = timezone('America/New_York')
load_dotenv()
dburl = os.environ.get('dburl')

header = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, zstd, utf-8',
    'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With': 'XMLHttpRequest'
}

data = {
    'country[]': '5',
    'sector': '36,25,27,28,24,29,35,30,26,34,33,31,32',
    'industry': '182,190,204,199,212,177,172,207,214,217,179,184,203,181,185,197,222,215,220,202,200,187,229,209,210,192,195,193,228,206,218,205,208,194,183,196,178,230,225,223,216,173,174,180,188,201,211,232,186,226,175,227,231,213,219,198,221,191,189,176,224',
    'equityType': 'ORD,DRC,Preferred,Unit,ClosedEnd,REIT,ELKS,OpenEnd,Right,ParticipationShare,CapitalSecurity,PerpetualCapitalSecurity,GuaranteeCertificate,IGC,Warrant,SeniorNote,Debenture,ETF,ADR,ETC',
    'exchange[]': '2',
    'eq_market_cap[min]': '1',
    'eq_market_cap[max]': '999999999999999',
    'pn': '1',
    'order[col]': 'eq_market_cap',
    'order[dir]': 'd'
}

res = requests.post('https://www.investing.com/stock-screener/Service/SearchStocks', headers=header, data=data)

if res.status_code == 200:
    content = res.content.decode('utf-8')
    body = json.loads(content)
    sortedList = sorted(body.get('hits'), key=lambda student: student.get('eq_market_cap'), reverse=True)
    eq_mkt_cap = sortedList[0].get('eq_market_cap')
    mktcap = sortedList[0].get('mktcap')

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

        session.add(MarketCapHistoricalData(symbol=symbol, date=marketTime, market_cap=marketCap))

    session.commit()
