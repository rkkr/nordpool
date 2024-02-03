import requests
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

API_URL = 'https://www.nordpoolgroup.com/api/marketdata/page/53?currency=,EUR,,EUR'
TIMEOUT = 60

def _parse_dt(date, time, fold):
    _date = datetime.strptime(date, '%d-%m-%Y').date()
    _time = datetime.fromisoformat(time).time()
    _datetime = datetime.combine(_date, _time, ZoneInfo('Europe/Stockholm'))
    if fold:
        # duplicate rows when daylight saving rotates
        _datetime = _datetime.replace(fold=1)

    return _datetime.astimezone(timezone.utc)

def download(end_date: datetime = None):
    json = _fetch_json(end_date)
    data = _parse_json(json)
    return data

def _fetch_json(end_date: datetime = None):
    url = API_URL if end_date == None else API_URL + '&endDate=' + end_date.strftime('%d-%m-%Y')
    response = requests.get(url, timeout=TIMEOUT)
    return response.json()

def _parse_json(json):
    _hour_prices = []
    _prev_time = None

    for row in json['data']['Rows']:
        if row['IsExtraRow']:
            continue
        _time = row['StartTime']

        for column in row['Columns']:
            if column['Value'] == "-":
                continue

            _date = column['Name']
            _datetime = _parse_dt(_date, _time, _prev_time == _time)
            _price = float(column['Value'].replace(' ', '').replace(',', '.'))
            _hour_prices.append({'datetime': _datetime, 'price_np': _price})

        _prev_time = _time

    _hour_prices.sort(key=lambda x: x['datetime'])

    return _hour_prices
