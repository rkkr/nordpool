import os, sys
from datetime import datetime, timedelta

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(DIR_PATH))
from crawler import nordpool, ignitis

OUT_CSV = os.path.join(os.path.dirname(DIR_PATH), 'prices.csv')

if __name__ == "__main__":
    start_date = datetime.strptime('2023-12-30', '%Y-%m-%d')
    end_date = datetime.strptime('2024-02-01', '%Y-%m-%d')
    prices = []

    while start_date < end_date:
        prices.extend(nordpool.download(end_date))
        end_date = end_date - timedelta(days=8)

    prices.sort(key=lambda x: x['datetime'])
    ignitis.add_price(prices)

    with open(OUT_CSV, 'w') as write:
        write.write('datetime;price;price_np\n')
        for row in prices:
            write.write(str(row['datetime']) + ';' + str(row['price']) + ';' + str(row['price_np']) + '\n')
