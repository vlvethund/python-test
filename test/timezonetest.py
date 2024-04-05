from datetime import datetime, timedelta

from pytz import timezone

tz = timezone('EST')

symbol = 'AAPL'
start = '2000-01-01'
end = 'today'

startSplit = start.split('-')

startDateTime = datetime(int(startSplit[0]), int(startSplit[1]), int(startSplit[2]), 0, 0, 0, tzinfo=tz)
endDateTime = datetime.today().astimezone(tz)
nextDateTime = startDateTime
while True:
    if nextDateTime < endDateTime:
        print(nextDateTime)
        nextDateTime = nextDateTime + timedelta(days=365)
    else:
        print(endDateTime)
        break

