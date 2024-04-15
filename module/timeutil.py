from datetime import datetime
from dateutil.relativedelta import relativedelta

from pytz import timezone

YEAR = 365


def get_edt_timezone():
    return timezone('America/New_York')


def get_year_range(start_date, end_date):
    arr = []

    if (end_date - start_date).days < 0:
        print('get_year_range error: start_date must be earlier than end_date')
        return arr

    if (end_date - start_date).days <= YEAR:
        arr.append({'start': start_date, 'end': end_date})
    else:
        while start_date <= end_date:
            next_start_date = start_date + relativedelta(years=1)
            if (end_date - start_date).days <= YEAR:
                arr.append({'start': start_date, 'end': end_date})
                break
            else:
                arr.append({'start': start_date, 'end': start_date + relativedelta(years=1, days=-1)})
            start_date = next_start_date
    return arr


def get_date_from_unix(unix_time):
    datetime.fromtimestamp(unix_time, get_edt_timezone())


if __name__ == '__main__':
    year_range = get_year_range(datetime(2000, 1, 1), datetime(2020, 8, 22))
    print(year_range)
