import nordpool, taxes, cache
import os, logging
from datetime import datetime, timedelta, timezone

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(filename=os.path.join(os.path.dirname(DIR_PATH), 'log.txt'), filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

if __name__ == "__main__":
    try:
        if cache.needs_update():
            logging.info('Updating cache')

            prices = nordpool.download(datetime.now(timezone.utc) + timedelta(days = 1))
            prices = taxes.add_price(prices)
            cache.save(prices)
    except Exception as e:
        logging.exception('Exception')
