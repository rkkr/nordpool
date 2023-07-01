import nordpool, ignitis, cache

if __name__ == "__main__":
    if cache.needs_update():
        print('Updating cache')

        prices = nordpool.download()
        prices = ignitis.add_price(prices)
        cache.save(prices)

    prices = cache.read()

    for price in prices:
        print(price)