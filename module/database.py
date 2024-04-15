from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from datetime import datetime
from timeutil import get_edt_timezone
from store.stockpricehistoricaldata import stock_price_historical_data
from sqlalchemy import and_
from module.yahoofinance import get_stock_historical_data


def connectdb():
    load_dotenv()
    db_url = os.environ.get('db_url')
    engine = create_engine(f'mysql+pymysql://{db_url}')
    return get_session(engine)


def get_session(engine):
    session = sessionmaker()
    session.configure(bind=engine)

    return session()


def save_stock_historical_data_list(content, session=connectdb()):
    tz = get_edt_timezone()

    insert_arr = []
    date_arr = []
    query_dict = {}
    symbol = content['chart']['result'][0]['meta']['symbol']

    for idx, unix_time in enumerate(content['chart']['result'][0]['timestamp']):
        date = datetime.fromtimestamp(unix_time, tz)
        open_price = content['chart']['result'][0]['indicators']['quote'][0]['open'][idx]
        high_price = content['chart']['result'][0]['indicators']['quote'][0]['high'][idx]
        low_price = content['chart']['result'][0]['indicators']['quote'][0]['low'][idx]
        close_price = content['chart']['result'][0]['indicators']['quote'][0]['close'][idx]
        volume = content['chart']['result'][0]['indicators']['quote'][0]['volume'][idx]
        adjclose = content['chart']['result'][0]['indicators']['adjclose'][0]['adjclose'][idx]

        date_arr.append(date.date())
        insert_arr.append(stock_price_historical_data(symbol=symbol, date=date, open=open_price,
                                                      high=high_price, low=low_price, close=close_price,
                                                      adj_close=adjclose, volume=volume))

    query_result = session.query(stock_price_historical_data).filter(
        and_(stock_price_historical_data.symbol == symbol, stock_price_historical_data.date.in_(date_arr))).all()

    for stock_data in query_result:
        query_dict[f'{stock_data.symbol}||{stock_data.date}'] = stock_data

    insert_arr = list(filter(lambda x: not (f'{x.symbol}||{x.date.date()}' in query_dict), insert_arr))

    sqlalchemy_session.add_all(insert_arr)
    sqlalchemy_session.commit()


if __name__ == '__main__':
    sqlalchemy_session = connectdb()
    print(sqlalchemy_session)
    target_symbol = 'AAPL'
    start = datetime(2024, 1, 1)
    end = datetime.today()

    historical_data = get_stock_historical_data(target_symbol, start, end)
    data = historical_data.json()
    save_stock_historical_data_list(data)
