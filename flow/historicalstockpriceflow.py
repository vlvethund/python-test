import string
from datetime import datetime

from module import timeutil, yahoofinance, logger, stockpricehistoricaldata


def collect_historical_stock_price_data(symbol: string, start: datetime, end: datetime):
    period = timeutil.get_year_range(start, end)

    for year in period:
        year_start = year.get('start')
        year_end = year.get('end')

        logger.info('-----------------------------------------------------------')
        logger.info(symbol + ': ', year_start.date(), '~', year_end.date())

        stock_data_res = yahoofinance.get_stock_historical_data(symbol, year_start, year_end)

        if stock_data_res.status_code != 200:
            logger.error('Stock Price Historical Data Response Error', stock_data_res.reason, f'Parmas: {symbol}, {year_start.date()}, {year_end.date()}')
            continue

        stock_data_body = stock_data_res.json()

        if stock_data_body['chart']['result'] is None:
            logger.error(logger.error(stock_data_body['chart']['error']['description']))
            continue

        stockpricehistoricaldata.save_stock_historical_data_from_yahoofinance(stock_data_body)
        logger.info('-----------------------------------------------------------')


def collect_historical_stock_price_data_with_symbols(symbols: list, start: datetime, end: datetime):
    for symbol in symbols:
        collect_historical_stock_price_data(symbol, start, end)


if __name__ == '__main__':
    stock_symbols = ['AAPL', 'MSFT', 'GOOG', 'XOM', 'WMT', 'GE', 'CSCO', '^IXIC']
    start_date = datetime(1980, 1, 1, 0, 0, 0, tzinfo=timeutil.get_edt_timezone())
    end_date = datetime.today().astimezone(timeutil.get_edt_timezone())
    collect_historical_stock_price_data_with_symbols(stock_symbols, start_date, end_date)
