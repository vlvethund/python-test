from sqlalchemy import tuple_
import copy

from module.database import connectdb
from module.timeutil import get_gmt_date_from_unix, get_date_from_unix
from module import logger
from store.marketcaphistocialdataentity import MarketCapHistoricalData


def save_market_cap_historical_data_from_yahoofinance(content):
    market_cap_historical_data_list = []

    for item in content.get('finance').get('result')[0].get('quotes'):
        symbol = item.get('symbol')
        market_unix_time = item.get('regularMarketTime').get('raw')
        market_time = get_date_from_unix(market_unix_time)
        market_cap = item.get('marketCap').get('raw')

        entity = MarketCapHistoricalData(symbol=symbol, date=market_time, market_cap=market_cap)
        market_cap_historical_data_list.append(entity)

    copy_list = copy.deepcopy(market_cap_historical_data_list)
    save_market_cap_historical_data(market_cap_historical_data_list)
    return copy_list


def save_market_cap_historical_data_from_ychart(content):
    market_cap_historical_data_list = []

    symbol = content.get('chart_data')[0][0].get('object_id')

    for item in content.get('chart_data')[0][0].get('raw_data'):
        date = get_gmt_date_from_unix(item[0] / 1000.0)
        market_cap = None
        if item[1] is float:
            market_cap = int(item[1] * 1000000)
        market_cap_historical_data_list.append(MarketCapHistoricalData(symbol=symbol, date=date, market_cap=market_cap))

    save_market_cap_historical_data(market_cap_historical_data_list)


def save_market_cap_historical_data(market_cap_list, session=connectdb()):
    pk_arr = []
    query_dict = {}

    for entity in market_cap_list:
        pk_arr.append((entity.symbol, entity.date.date()))

    query_result = session.query(MarketCapHistoricalData) \
        .filter(tuple_(MarketCapHistoricalData.symbol, MarketCapHistoricalData.date).in_(pk_arr)).all()

    for cap_data in query_result:
        query_dict[f'{cap_data.symbol}||{cap_data.date}'] = cap_data

    insert_arr = list(filter(lambda x: not (f'{x.symbol}||{x.date.date()}' in query_dict), market_cap_list))

    logger.info(f'Input Market Cap Entities Amount: {len(market_cap_list)}')
    logger.info(f'Filtered Market Cap Entities Amount: {len(market_cap_list) - len(insert_arr)}')
    logger.info(f'Saving Market Cap Entities Amount: {len(insert_arr)}')

    session.add_all(insert_arr)
    session.commit()
