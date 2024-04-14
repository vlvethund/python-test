import os
import json
from datetime import datetime, timedelta

from dotenv import load_dotenv
from pytz import timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from feature import get_data, save_data

# inputs
symbol = 'AAPL'
# symbol = 'MSFT'
# symbol = 'GOOG'
# symbol = 'XOM'
# symbol = 'WMT'
# symbol = 'GE'
# symbol = 'CSCO'
# symbol = 'IXIC'
start = '2024-04-12'
end = 'today'


def get_historical_data(symbol, start, end):
    # db settings
    load_dotenv()
    dburl = os.environ.get('dburl')

    engine = create_engine(
        f'mysql+pymysql://{dburl}')

    Session = sessionmaker()
    Session.configure(bind=engine)

    session = Session()

    # time settings

    tz = timezone('America/New_York')
    startSplit = start.split('-')

    startDateTime = datetime(int(startSplit[0]), int(startSplit[1]), int(startSplit[2]), 0, 0, 0, tzinfo=tz)
    endDateTime = datetime.today().astimezone(tz)

    if end != 'today':
        endSplit = end.split('-')
        endDateTime = datetime(int(endSplit[0]), int(endSplit[1]), int(endSplit[2]), 0, 0, 0, tzinfo=tz)

    sectionStartDateTime = startDateTime
    sectionEndDateTime = startDateTime + timedelta(days=365)

    while True:
        if sectionEndDateTime < endDateTime:
            response = get_data(symbol, sectionStartDateTime, sectionEndDateTime)

            if response.status_code != 200:
                print('Request Error', response.reason)

                sectionStartDateTime = sectionEndDateTime + timedelta(days=1)
                sectionEndDateTime = sectionEndDateTime + timedelta(days=366)
                continue

            content = response.content.decode('utf-8')
            data = json.loads(content)

            if data['chart']['result'] is None:
                print(content['chart']['error']['description'])
                sectionStartDateTime = sectionEndDateTime + timedelta(days=1)
                sectionEndDateTime = sectionEndDateTime + timedelta(days=366)
                continue

            print(f'Saving {sectionStartDateTime.date()} - {sectionEndDateTime.date()}...')
            save_data(data, session)

            sectionStartDateTime = sectionEndDateTime + timedelta(days=1)
            sectionEndDateTime = sectionEndDateTime + timedelta(days=366)
        else:
            response = get_data(symbol, sectionStartDateTime, sectionEndDateTime)

            if response.status_code != 200:
                print('Request Error', response.reason)
                continue
            content = response.content.decode('utf-8')
            data = json.loads(content)

            if data['chart']['result'] is None:
                print(content['chart']['error']['description'])
                continue

            print(f'Saving {sectionStartDateTime.date()} - {sectionEndDateTime.date()}...')
            save_data(data, session)
            break


# get_historical_data(symbol, start, end)
