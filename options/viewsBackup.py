from django.shortcuts import render
import yahooquery
import requests
import json
from yahooquery import Ticker
import time
import json
import requests
import pandas as pd

#start of tradingView bits
def tradingView(
    mktCapMin = 5000000000,
    div_yield_recent = 2,
    StochK = 25,
    StochD = 25,
    macd_macd = 0,
    macd_signal = 0,
):
    global tradingViewTime
    startTime = time.time()
    filter = [
        {
            "left": "volume",
            "operation": "nempty"
        },
        {
            "left": "type",
            "operation": "in_range",
            "right": [
                "stock",
                "dr",
                "fund"
            ]
        },
        {
            "left": "subtype",
            "operation": "in_range",
            "right": [
                "common",
                "foreign-issuer",
                "",
                "etf",
                "etf,odd",
                "etf,otc",
                "etf,cfd"
            ]
        },
        {
            "left": "exchange",
            "operation": "in_range",
            "right": [
                "AMEX",
                "NASDAQ",
                "NYSE"
            ]
        },
        {
            "left": "market_cap_basic",
            "operation": "egreater",
            "right": mktCapMin
        },
        {
            "left": "is_primary",
            "operation": "equal",
            "right": True
        },
        {
            "left": "Stoch.K",
            "operation": "less",
            "right": StochK
        },
        {
            "left": "Stoch.D",
            "operation": "less",
            "right": StochD
        },
        {
            "left": "MACD.macd",
            "operation": "less",
            "right": macd_macd
        },
        {
            "left": "MACD.signal",
            "operation": "less",
            "right": macd_signal
        },
        {
            "left": "dividend_yield_recent",
            "operation": "egreater",
            "right": div_yield_recent
        },
        {
            "left": "Stoch.RSI.K",
            "operation": "less",
            "right": 25
        },
        {
            "left": "Stoch.RSI.D",
            "operation": "less",
            "right": 25
        }
    ]
    options = {
        "lang": "en"
    }
    markets = {
        "america"
    }
    symbols = {
        "query": {
            "types": []
        },
        "tickers": []
    }
    columns = [
        #"logoid",
        "name",
        "description",
        "close",
        "change",
        "change_abs",
        "Recommend.All",
        "market_cap_basic",
        "price_earnings_ttm",
        "earnings_per_share_basic_ttm",
        "sector",
        "earnings_release_date",
        "earnings_release_next_date",
        "dividend_yield_recent"
    ]
    sort = {
        "sortBy": "volume",
        "sortOrder": "desc"
    }
    range = [
        0,
        150
    ]

    post_message = {}
    post_message['filter'] = filter
    post_message['options'] = options
    post_message['symbols'] = symbols
    post_message['columns'] = columns
    post_message['sort'] = sort
    post_message['range'] = range

    payload = json.dumps(post_message)


    url = "https://scanner.tradingview.com/america/scan"
    #     payload = self.payload
    headers = {
        'authority': 'scanner.tradingview.com',
        'accept': 'text/plain, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https//www.tradingview.com',
        'referer': 'https//www.tradingview.com/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    response_json = response.json()['data']

    df0 = pd.DataFrame.from_dict(response_json)
    df0.drop(columns=['s'], inplace=True)
    df = pd.DataFrame(df0["d"].to_list(), columns=columns)
#     display(df)

    df['change'] = df['change'].round(2)
    df['dividend_yield_recent'] = df['dividend_yield_recent'].round(2)
    df['price_earnings_ttm'] = df['price_earnings_ttm'].round(2)
    df['earnings_per_share_basic_ttm'] = df['earnings_per_share_basic_ttm'].round(2)
#     display(df)
    myTickers = df['name'].to_dict()
#     executionTime = (time.time() - startTime)
#     tradingViewTime = tradingViewTime + executionTime
    results = myTickers

    # return render(request, 'options/options.html', results)
    return results

# Create your views here.
def index(request):

    ticker = 'aapl'
    yq_ticker = Ticker(ticker)
    quotes = yq_ticker.price

    myTickers = tradingView()
    results = {'quotes': quotes, 'myTickers': myTickers}

    return render(request, 'options/options.html', results)




#function for getting current price of ticker
def getCurrentPrice(ticker):
    global getCurrentPriceTime
    startTime = time.time()

    yq_ticker = Ticker(ticker)
    #may contain EPS and shares outstanding
    quotes = yq_ticker.quotes[ticker]

    currentPrice = (quotes['bid'] + quotes['ask'])/2
#     print('epsCurrentYear: ', quotes['epsCurrentYear'])
#     print('sharesOutstanding', quotes['sharesOutstanding'])

#     print('important thing is price, date ticker')
#     print(ticker, 'currentPrice: ',  currentPrice)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    groupA = [[now, ticker, currentPrice]]
    groupA_cols = ['dateTime', 'ticker', 'currentPrice']
    livePrice_dfA = pd.DataFrame(groupA, columns = groupA_cols)
    
    executionTime = (time.time() - startTime)
    getCurrentPriceTime = getCurrentPriceTime + executionTime
    
    return livePrice_dfA