import jinja2, os, sys
from datetime import datetime, timedelta

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(DIR_PATH, 'index.html')

sys.path.append(os.path.dirname(DIR_PATH))
from crawler import cache

def get_days():
    today = datetime.now().date()
    return [today + timedelta(days=1), today, today - timedelta(days=1)]

def format_prices(prices):
    for price in prices:
        price['day'] = price['datetime'].astimezone().date()
        price['hour'] = price['datetime'].astimezone().hour
    return prices

def get_avg(prices):
    month = datetime.now().month
    month_prices = [p['price'] for p in prices if p['datetime'].month == month]
    return sum(month_prices) / len(month_prices)

def render():
    with open(TEMPLATE_PATH, 'r') as read:
        template = jinja2.Template(read.read())

    days = get_days()
    prices = cache.read()
    prices = format_prices(prices)
    month_avg = get_avg(prices)
    return template.render({'prices': prices, 'days': days, 'avg': month_avg})

def handler(req):
    from mod_python import apache

    req.content_type = 'text/html'
    req.send_http_header()
    req.write(render())

    return apache.OK

if __name__ == "__main__":
    with open(os.path.join(DIR_PATH, 'render.html'), 'w') as write:
        write.write(render())
