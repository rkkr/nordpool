import nordpool, ignitis, cache
import os, logging

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(filename=os.path.join(DIR_PATH, 'crawler.log'), filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    try:
        if cache.needs_update():
            logging.info('Updating cache')

            prices = nordpool.download()
            prices = ignitis.add_price(prices)
            cache.save(prices)
        else:
            logging.info('Cache up to date')
    except Exception as e:
        logging.excepetion('Exception')
