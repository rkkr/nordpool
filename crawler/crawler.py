import nordpool, ignitis, cache, logging

logging.basicConfig(filename='crawler.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

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
