import os
from datetime import datetime

import requests
from dotenv import load_dotenv
from pytz import timezone

tz = timezone('America/New_York')
load_dotenv()
dburl = os.environ.get('dburl')

symbol = 'AAPL'
start = '04/01/2024'
end = '04/12/2024'

headers = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "ycsessionid=q4i61h698nbaetqk14klk0f0cbw9somb;",
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.0.3705;)',
    'X-Requested-With': 'XMLHttpRequest'
}

body = {
    "calcs": "id:market_cap,include:true,,",
    "securities": f"id:{symbol},include:true,,",
    "startDate": start,
    "endDate": end,
    "chartId": "",
    "chartType": "interactive",
    "correlations": "",
    "customGrowthAmount": "",
    "dataInLegend": "value",
    "dateSelection": "range",
    "displayDateRange": "false",
    "format": "real",
    "legendOnChart": "false",
    "lineAnnotations": f"{symbol}:::market_cap::area_chart:false,avg:false,dividends:false,earnings_results:false,force_on_single_panel:false,force_original:false,hidden:false,max:false,min:false,spinoffs:false,splits:true",
    "nameInLegend": "name_and_ticker",
    "note": "",
    "partner": "basic_2000",
    "quoteLegend": "false",
    "recessions": "false",
    "scaleType": "linear",
    "securityGroup": "",
    "securitylistName": "",
    "securitylistSecurityId": "",
    "source": "false",
    "splitType": "single",
    "title": "",
    "units": "false",
    "useCustomColors": "false",
    "useEstimates": "false",
    "zoom": "",
    "redesign": "true",
    "chartCreator": "false",
    "maxPoints": "554",
}

res = requests.post('https://ycharts.com/charts/fund_data.json', headers=headers, data=body)

raw_data = res.json().get('chart_data')[0][0].get('raw_data')

for data in raw_data:
    data_datetime = datetime.fromtimestamp(data[0] / 1000.0, tz)
    print(data[0] / 1000.0)
    print(data_datetime)
    print(data[1])
    print('--------------------------')

# print(res)
