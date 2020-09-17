import pandas as pd
import requests
import json
import time
import asyncio
from datetime import datetime as dt


coins = {'BTC': 'Bitcoin', 'ETH': 'Ethereum', 'LTC': 'Litecoin',
         'XRP': 'Ripple', 'USDT': 'Tether'
         }


def get_apikey():
    with open('alphavantageapi.key', 'r') as f:
        return str(f.readline().strip())


def assemble_url(currency: str, wapi_key: str):
    wurl = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE"
    return "".join([wurl, "&from_currency=", currency,
                    "&to_currency=EUR&apikey=", wapi_key])


def send_request(url: str):
    return requests.get(url).text


def read_currencies():
    cur = pd.read_csv('digital_currency_list.csv', names=[
                      'id', 'desc'], skiprows=[0, 3]).to_dict(orient='list')
    # cur['id'][index], cur['desc'][index]
    d = dict()
    for key, value in zip(cur['id'], cur['desc']):
        d[key] = value
    return d


def main():
    # start_time = time.perf_counter()
    wapi_key = get_apikey()
    for i in coins.keys():
        obj = json.loads(send_request(assemble_url(i, wapi_key)))
        if obj.get('Error Message') is None:
            currency_id = obj.get('Realtime Currency Exchange Rate')[
                '1. From_Currency Code']
            currency_desc = obj.get('Realtime Currency Exchange Rate')[
                '2. From_Currency Name']
            date = obj.get('Realtime Currency Exchange Rate')[
                '6. Last Refreshed']
            bid_price = obj.get('Realtime Currency Exchange Rate')[
                '8. Bid Price']
            ask_price = obj.get('Realtime Currency Exchange Rate')[
                '9. Ask Price']
            rate = obj.get('Realtime Currency Exchange Rate')[
                '5. Exchange Rate']
            print(currency_id, currency_desc, date, bid_price, ask_price, rate)
        else:
            print('exit 1', dt.now(), obj['Error Message'])
#    print(f"Executed in {time.perf_counter() - start_time:.2f}s")


if __name__ == '__main__':
    main()
