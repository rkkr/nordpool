import json, os
from datetime import datetime, timedelta, timezone

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
PRICE_PATH = os.path.join(os.path.dirname(DIR_PATH), 'prices.json')

def save(prices):
    with open(PRICE_PATH, 'w') as write:
        json.dump(prices, write, indent = 4, default = str)

def read():
    with open(PRICE_PATH, 'r') as read:
        prices = json.load(read)

    for price in prices:
        price['datetime'] = datetime.fromisoformat(price['datetime'])

    return prices

def needs_update():
    if not os.path.isfile(PRICE_PATH):
        return True

    prices = read()
    if len(prices) == 0:
        return True
    max_datetime = max(x['datetime'] for x in prices)
    return max_datetime - timedelta(hours = 10) < datetime.now(timezone.utc)
