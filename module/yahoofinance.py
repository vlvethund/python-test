import requests
import json


def get_stock_historical_data(symb, start, end):
    start_unix = int(start.timestamp())
    end_unix = int(end.timestamp())

    url = (f'https://query2.finance.yahoo.com/v8/finance/chart/{symb}'
           f'?formatted=true&crumb=BAeTUdnAlvz&lang=en-US&region=US&includeAdjustedClose=true&interval=1d&'
           f'period1={start_unix}&'
           f'period2={end_unix}&events=capitalGain%7Cdiv%7Csplit&useYfid=true&corsDomain=finance.yahoo.com')

    return requests.get(url, headers={'user-agent': 'sdfsdf', 'Accept': 'application/json, text/plain, */*'})


def get_current_top_market_cap(max_size=25):
    params = {
        'crumb': 'WFUUfvdDToA',
        'formatted': 'true'
    }

    headers = {
        'Cookie': 'axids=gam=y-Pkq14dtE2uJJK4bZFjz7ZgWv.w.CXYar~A&'
                  'dv360=eS0xUnp5SS5WRTJ1R1Z1VldPamt6dWxXYm5UWUs2Y2tNb35B'
                  '&ydsp=y-lIq6EctE2uI5CjVLu80uFBMLAOxJC8Jz~A&tbla=y-bTJc.o9E2uIN_5RcT5oezEMbkWAXICce~A; '
                  'tbla_id=485cdde1-664c-4ff0-b679-e784b56e8698-tuct9c00962; '
                  'GUC=AQEBCAFmENlmPkIa9gQN&s=AQAAAMI9yvd0&g=Zg-TgA; '
                  'A1=d=AQABBPKYxmICEP6o1TfN9QwGVFLyzmwoxHEFEgEBCAHZEGY-Zmdkb2UB_eMBAAcI8pjGYmwoxHE&'
                  'S=AQAAAiYrej3Yf-rUHYu4glyh3WU; '
                  'A3=d=AQABBPKYxmICEP6o1TfN9QwGVFLyzmwoxHEFEgEBCAHZEGY-Zmdkb2UB_eMBAAcI8pjGYmwoxHE&S=AQAAAiYrej3Yf-rUHYu4glyh3WU; '
                  'PRF=t%3D%255EIXIC%252BGE%252BXOM%252BGOOG%252BAAPL%252BCANQ%26newChartbetateaser%3D1; '
                  'A1S=d=AQABBPKYxmICEP6o1TfN9QwGVFLyzmwoxHEFEgEBCAHZEGY-Zmdkb2UB_eMBAAcI8pjGYmwoxHE&S=AQAAAiYrej3Yf-rUHYu4glyh3WU; '
                  'cmp=t=1712905314&j=0&u=1---; gpp=DBAA; gpp_sid=-1',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, utf-8, zstd',
        'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.0.3705;)',
        'X-Requested-With': 'XMLHttpRequest'
    }

    data = {"size": max_size, "offset": 0, "sortField": "intradaymarketcap", "sortType": "DESC", "quoteType": "EQUITY",
            "topOperator": "AND", "query": {"operator": "AND", "operands": [
            {"operator": "or", "operands": [{"operator": "EQ", "operands": ["region", "us"]}]},
            {"operator": "or", "operands": [{"operator": "GT", "operands": ["intradaymarketcap", 100000000000]}]}]},
            "userId": "", "userIdType": "guid"}

    return requests.post('https://query2.finance.yahoo.com/v1/finance/screener',
                         headers=headers,
                         data=json.dumps(data),
                         params=params)
