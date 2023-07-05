from miio import ChuangmiPlug
from config import config
import os, sys

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(DIR_PATH))
from crawler import cache

if __name__ == "__main__":
    prices = cache.read()

    for plugConfig in config:
        expected = plugConfig['schedule'].get_state(prices)
        plug = ChuangmiPlug(plugConfig['ip'], plugConfig['token'])
        current = plug.status().power
        print('Plug ' + plugConfig['name'] + ' expected: ' + str(expected) + ' current: ' + str(current))

        if expected != current:
            plug.on() if expected else plug.off()
