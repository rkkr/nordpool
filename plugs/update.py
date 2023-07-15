from miio import ChuangmiPlug
from config import config
import os, sys, logging

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(DIR_PATH))
from crawler import cache

logging.basicConfig(filename=os.path.join(os.path.dirname(DIR_PATH), 'log.txt'), filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

if __name__ == "__main__":
    prices = cache.read()

    for plugConfig in config:
        if plugConfig['schedule'] is None:
            continue

        try:
            expected = plugConfig['schedule'].get_state(prices)
            plug = ChuangmiPlug(plugConfig['ip'], plugConfig['token'])
            current = plug.status().power

            if expected != current:
                if expected:
                    logging.info('Turning on %s', plugConfig['name'])
                    result = plug.on()
                else:
                    logging.info('Turning off %s', plugConfig['name'])
                    result = plug.off()
                logging.info('Result: %s', result)
        except Exception as e:
            logging.exception('Exception')
