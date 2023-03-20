from requests import Session
import json


def print_price():
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    parameters = {
        'slug': 'usd',
        'convert': 'RUB'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'YOUR API TOKEN'
    }

    session = Session()
    session.headers.update(headers)
    response = session.get(url, params=parameters)
    return str(json.loads(response.text)['data']['20317']['quote']['RUB']['price'])[:6]
