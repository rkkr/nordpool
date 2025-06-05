import jinja2, os, sys, datetime

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(DIR_PATH, 'index.html')

sys.path.append(os.path.dirname(DIR_PATH))
from crawler import cache

def format_prices(prices):
    recent = datetime.datetime.now(datetime.UTC).replace(minute=0, second=0, microsecond=0)
    prices = [p for p in prices if p['datetime'] >= recent]
    for price in prices:
        _datetime = price['datetime'].astimezone()
        price['hour'] = f"{_datetime.date()} {_datetime.hour:02}"
    return prices

def get_hours(prices):
    dist = list(set([p['hour'] for p in prices]))
    dist.sort()
    return dist

def render():
    with open(TEMPLATE_PATH, 'r') as read:
        template = jinja2.Template(read.read())

    prices = cache.read()
    formatted = format_prices(prices)
    hours = get_hours(formatted)
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
