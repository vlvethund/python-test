from datetime import datetime

from sqlalchemy import tuple_

from module.database import connectdb
from module.yahoofinance import get_stock_historical_data
from store.stockpricehistoricaldataentity import StockPriceHistoricalData
from module.timeutil import get_date_from_unix
from module import logger


def save_stock_historical_data_from_yahoofinance(content):
    stock_historical_data_list = []
    symbol = content['chart']['result'][0]['meta']['symbol']

    for idx, unix_time in enumerate(content['chart']['result'][0]['timestamp']):
        date = get_date_from_unix(unix_time)
        open_price = content['chart']['result'][0]['indicators']['quote'][0]['open'][idx]
        high_price = content['chart']['result'][0]['indicators']['quote'][0]['high'][idx]
        low_price = content['chart']['result'][0]['indicators']['quote'][0]['low'][idx]
        close_price = content['chart']['result'][0]['indicators']['quote'][0]['close'][idx]
        volume = content['chart']['result'][0]['indicators']['quote'][0]['volume'][idx]
        adjclose = content['chart']['result'][0]['indicators']['adjclose'][0]['adjclose'][idx]

        stock_historical_data_list.append(StockPriceHistoricalData(symbol=symbol, date=date, open=open_price,
                                                                   high=high_price, low=low_price, close=close_price,
                                                                   adj_close=adjclose, volume=volume))

    return save_stock_historical_data_list(stock_historical_data_list)


def save_stock_historical_data_list(stock_historical_data_list, session=connectdb()):
    pk_arr = []
    query_dict = {}

    for entity in stock_historical_data_list:
        pk_arr.append((entity.symbol, entity.date.date()))

    query_result = session.query(StockPriceHistoricalData) \
        .filter(tuple_(StockPriceHistoricalData.symbol, StockPriceHistoricalData.date).in_(pk_arr)).all()

    for stock_data in query_result:
        query_dict[f'{stock_data.symbol}||{stock_data.date}'] = stock_data

    insert_arr = list(filter(lambda x: not (f'{x.symbol}||{x.date.date()}' in query_dict), stock_historical_data_list))

    logger.info(f'Input Stock Data Entities Amount: {len(stock_historical_data_list)}')
    logger.info(f'Filtered Stock Data Entities Amount: {len(stock_historical_data_list) - len(insert_arr)}')
    logger.info(f'Saving Stock Data Entities Amount: {len(insert_arr)}')

    session.add_all(insert_arr)
    session.commit()
    return insert_arr


if __name__ == '__main__':
    target_symbol = 'AAPL'
    start = datetime(2024, 1, 1)
    end = datetime.today()

    historical_data = get_stock_historical_data(target_symbol, start, end)
    data = historical_data.json()
    save_stock_historical_data_from_yahoofinance(data)
