import json

import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

wallet_sol = 23
TOKEN = "6031223771:AAHAaWDFmHMPPxpLce7Bc_LZuLa-8ebGFQg"
chat_id = "125068330"


def get_usd():
    try:
        response = requests.get('https://v6.exchangerate-api.com/v6/5249cba917aedca9c89323dd/latest/USD')
        currency = response.json()['conversion_rates']['RUB']
    except (ConnectionError, Timeout, TooManyRedirects):
        currency = None
    return float(currency)


def get_sol():
    try:
        response = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest', params={'slug': 'solana'}, headers={'X-CMC_PRO_API_KEY': '810bc9fc-7dfc-4909-882a-66d53fda7934'})
        currency = json.loads(response.text)['data']['5426']['quote']['USD']['price']
    except (ConnectionError, Timeout, TooManyRedirects):
        currency = None
    return float(currency)


def send_to_telegram(token, chat_id, message):
    return requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}").json()


currency_sol = get_sol()
currency_usd = get_usd()
wallet = wallet_sol * currency_sol * currency_usd
message = f'SOL: {currency_sol} USD\nUSD: {currency_usd} RUB\nWALLET: {wallet} RUB'
send_to_telegram(token=TOKEN, chat_id=chat_id, message=message)