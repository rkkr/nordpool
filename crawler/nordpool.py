import requests
from datetime import datetime

API_URL = 'https://dataportal-api.nordpoolgroup.com/api/DayAheadPrices?date=%s&market=DayAhead&deliveryArea=LT&currency=EUR'
TIMEOUT = 60

def download(date: datetime):
    json = _fetch_json(date)
    data = _parse_json(json)
    return data

def _fetch_json(date: datetime):
    url = API_URL % date.strftime('%Y-%m-%d')
    response = requests.get(url, timeout=TIMEOUT)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def _parse_json(json):
    if json is None:
        return None
    if json['areaStates'][0]['state'] != 'Final':
        return None
    _hour_prices = []

    for row in json['multiAreaEntries']:
        _datetime = datetime.fromisoformat(row['deliveryStart'])
        _price = row['entryPerArea']['LT']
        _hour_prices.append({'datetime': _datetime, 'price_np': _price})

    _hour_prices.sort(key=lambda x: x['datetime'])

    return _hour_prices
