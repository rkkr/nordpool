from miio import ChuangmiPlug, DeviceException
from config import config
import os, sys, logging, time

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(DIR_PATH))
from crawler import cache

logging.basicConfig(filename=os.path.join(os.path.dirname(DIR_PATH), 'log.txt'), filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def update_plug(plugConfg, expectedState, retries = 5):
    try:
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
    except DeviceException:
        if retries == 0:
            raise

        time.sleep(5)
        update_plug(plugConfg, expectedState, retries - 1)

if __name__ == "__main__":
    prices = cache.read()

    for plugConfig in config:
        if plugConfig['schedule'] is None:
            continue

        expected = plugConfig['schedule'].get_state(prices)

        try:
            update_plug(plugConfig, expected)
        except Exception as e:
            logging.exception('Exception')
