from module import marketcaphistoricaldata, stockpricehistoricaldata, yahoofinance, logger


def collect_daily_data():
    logger.info('[[[ DAILY TASK START ]]]')
    logger.info('Get Current Top Market Cap Data from Yahoo Finance..')
    top_market_cap_res = yahoofinance.get_current_top_market_cap(10)

    if top_market_cap_res.status_code != 200:
        logger.error('Current Top Market Cap Res Error', top_market_cap_res.reason)
        return

    top_market_cap_body = top_market_cap_res.json()

    market_cap_entities = marketcaphistoricaldata.save_market_cap_historical_data_from_yahoofinance(top_market_cap_body)

    for market_cap_entity in market_cap_entities:
        symbol = market_cap_entity.symbol
        date = market_cap_entity.date

        logger.info('-----------------------------------------------------------')
        logger.info(f'Get Stock Price Historical Data of {symbol} at {date.date()}...')

        stock_historical_data_res = yahoofinance.get_stock_historical_data(symbol, date, date)
        stock_historical_data_body = stock_historical_data_res.json()

        if stock_historical_data_res.status_code != 200:
            logger.error('Stock Price Historical Data Response Error',
                         stock_historical_data_res.reason, f'Params: {symbol}, {date.date()}')
            continue

        if stock_historical_data_body['chart']['result'] is None:
            logger.error(logger.error(stock_historical_data_body['chart']['error']['description']))
            continue

        stockpricehistoricaldata.save_stock_historical_data_from_yahoofinance(stock_historical_data_res.json())
        logger.info('-----------------------------------------------------------')

    collect_nasdaq_composite(market_cap_entities[0].date)
    logger.info('[[[ DAILY TASK END ]]]')


def collect_nasdaq_composite(date):
    symbol='^IXIC'

    logger.info('-----------------------------------------------------------')
    logger.info(f'Get Nasdaq Composite Data ({symbol}) at {date.date()}...')

    nasdaq_res = yahoofinance.get_stock_historical_data(symbol, date, date)
    nasdaq_body = nasdaq_res.json()

    if nasdaq_res.status_code != 200:
        logger.error('Stock Price Historical Data Response Error',
                     nasdaq_res.reason, f'Params: {symbol}, {date.date()}')
        return

    if nasdaq_body['chart']['result'] is None:
        logger.error(logger.error(nasdaq_body['chart']['error']['description']))
        return

    stockpricehistoricaldata.save_stock_historical_data_from_yahoofinance(nasdaq_body)
    logger.info('-----------------------------------------------------------')


if __name__ == '__main__':
    collect_daily_data()
