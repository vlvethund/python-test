from datetime import datetime
from pytz import timezone

tz = timezone('EST')
start = '2024-03-01'
print(datetime.now())
print(datetime.now(tz))
print(datetime.now().astimezone(tz))

startDateTime = datetime.strptime(start, '%Y-%m-%d').astimezone(tz)

print(startDateTime)

print(datetime(2024, 3, 1, 0, 0, 0, tzinfo=tz))

print(start.split('-'))