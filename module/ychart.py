import requests


def get_market_cap_historical_data(symbol, start, end):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": "ycsessionid=sc7642h9dytwlulei71g40469dxfthoh;",
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.0.3705;)',
        'X-Requested-With': 'XMLHttpRequest'
    }

    body = {
        "calcs": "id:market_cap,include:true,,",
        "securities": f"id:{symbol},include:true,,",
        "startDate": start.strftime('%m/%d/%Y'),
        "endDate": end.strftime('%m/%d/%Y'),
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

    return requests.post('https://ycharts.com/charts/fund_data.json', headers=headers, data=body)
