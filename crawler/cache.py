import json, os
from datetime import datetime

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
    
    try:
        prices = read()
        max_datetime = max(x['datetime'] for x in prices)
        now = datetime.utcnow()
        return max_datetime.date() == now.date() and now.hour > 13
    except:
        return True