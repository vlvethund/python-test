import string
from datetime import datetime
from module import timeutil, logger, ychart, marketcaphistoricaldata
from store.stock_list import target_symbol_list


def collect_historical_market_cap_data(symbol: string, start: datetime, end: datetime):
    period = timeutil.get_year_range(start, end)

    for year in period:
        year_start = year.get('start')
        year_end = year.get('end')

        logger.info('-----------------------------------------------------------')
        logger.info(symbol + ': ', year_start.date(), '~', year_end.date())

        market_cap_data_res = ychart.get_market_cap_historical_data(symbol, year_start, year_end)

        if market_cap_data_res.status_code != 200:
            logger.error('Stock Price Historical Data Response Error', market_cap_data_res.reason, f'Parmas: {symbol}, {year_start.date()}, {year_end.date()}')
            continue

        market_cap_data_body = market_cap_data_res.json()

        marketcaphistoricaldata.save_market_cap_historical_data_from_ychart(market_cap_data_body)

        logger.info('-----------------------------------------------------------')


def collect_historical_market_cap_data_with_symbols(symbols: list, start: datetime, end: datetime):
    for idx, symbol in enumerate(symbols):
        logger.info(f'Symbol: {symbol} ({idx} / {len(symbols)})')
        logger.info(f'Percentage Of Progress {idx/len(symbols) * 100}%')
        collect_historical_market_cap_data(symbol, start, end)


if __name__ == '__main__':

    # stock_symbols = ['AAPL', 'MSFT', 'GOOG', 'XOM', 'WMT', 'GE', 'CSCO', '^IXIC']
    # stock_symbols = ['^IXIC']
    start_date = datetime(1980, 1, 1, 0, 0, 0, tzinfo=timeutil.get_edt_timezone())
    end_date = datetime.today().astimezone(timeutil.get_edt_timezone())

    collect_historical_market_cap_data_with_symbols(target_symbol_list, start_date, end_date)
