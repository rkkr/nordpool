import jinja2, os, sys
from datetime import datetime, timedelta, timezone

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(DIR_PATH, 'index.html')

sys.path.append(os.path.dirname(DIR_PATH))
from crawler import cache

def filter_recent(prices):
    recent = datetime.now(timezone.utc) - timedelta(minutes = 15)
    prices = [p for p in prices if p['datetime'] >= recent]
    prices.sort(key=lambda price: price['datetime'])
    return prices

def format_prices(prices):
    formatted = {}
    for price in prices:
        _datetime = price['datetime']
        formatted[f"{_datetime.date()} {_datetime.hour:02}:{_datetime.minute:02}"] = price['price']
    return formatted

def get_hours(prices):
    output = []
    days = set()
    dayhours = set()
    for price in prices:
        _datetime = price['datetime']
        _key = f"{_datetime.date()} {_datetime.hour:02}"
        _day = f"{_datetime.astimezone().date()}"
        _hour = f"{_datetime.astimezone().hour:02}"
        _dayhour = _day + ' ' + _hour
        if _dayhour in dayhours:
            continue
        dayhours.add(_dayhour)
        if _day in days:
            _dayhour = _hour
        else:
            days.add(_day)
        output.append({'key': _key, 'display': _dayhour})
    
    return output

def render():
    with open(TEMPLATE_PATH, 'r') as read:
        template = jinja2.Template(read.read())

    prices = cache.read()
    prices = filter_recent(prices)
    hours = get_hours(prices)
    formatted = format_prices(prices)
    return template.render({'prices': formatted, 'hours': hours})

def handler(req):
    from mod_python import apache

    req.content_type = 'text/html'
    req.send_http_header()
    req.write(render())

    return apache.OK

if __name__ == "__main__":
    with open(os.path.join(DIR_PATH, 'render.html'), 'w') as write:
        write.write(render())
