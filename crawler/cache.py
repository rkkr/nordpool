import json, os
from datetime import datetime, timedelta, timezone

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
PRICE_PATH = os.path.join(os.path.dirname(DIR_PATH), 'prices.json')

def save(prices):
    if len(prices) == 0:
        return

    prices = prices + read()
    cleanup = datetime.now(timezone.utc) - timedelta(days = 90)
    prices = [p for p in prices if p['datetime'] > cleanup]

    with open(PRICE_PATH, 'w') as write:
        json.dump(prices, write, default = str)

def read():
    if not os.path.isfile(PRICE_PATH):
        return []

    with open(PRICE_PATH, 'r') as read:
        prices = json.load(read)

    for price in prices:
        price['datetime'] = datetime.fromisoformat(price['datetime'])

    return prices

def needs_update():
    prices = read()
    if len(prices) == 0:
        return True
    max_datetime = max(x['datetime'] for x in prices)
    return max_datetime - timedelta(hours = 12) < datetime.now(timezone.utc)
