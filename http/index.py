import jinja2, os, sys
from mod_python import apache

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(DIR_PATH, 'index.html')

sys.path.append(os.path.dirname(DIR_PATH))
from crawler import cache

def render():
    with open(TEMPLATE_PATH, 'r') as read:
        template = jinja2.Template(read.read())

    prices = cache.read()
    return template.render({'prices': prices})

def handler(req):
    req.content_type = 'text/html'
    req.send_http_header()
    req.write(render())

    return apache.OK
