import os, sys
from datetime import datetime, timezone, timedelta

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(DIR_PATH))
from crawler import nordpool

ESO_PATH = os.path.join(os.path.dirname(DIR_PATH), 'Valandiniai.csv')

def read_eso():
    usages = {}
    with open(ESO_PATH, 'r') as read:
        read.readline()
        for line in read.readlines():
            cols = line.strip('\n').split(';')
            date = datetime.fromisoformat(cols[-4].strip('"')).astimezone(timezone.utc)
            usage = float(cols[-1].strip('"'))
            usages[date] = {'usage': usage}
    
    return usages

if __name__ == "__main__":
    start_date = datetime.strptime('2024-09-30', '%Y-%m-%d')
    end_date = datetime.strptime('2024-11-15', '%Y-%m-%d')
    prices = []

    while start_date < end_date:
        prices.extend(nordpool.download(start_date))
        start_date = start_date + timedelta(days=1)

    eso = read_eso()

    total_usage = sum([eso[date]['usage'] for date in eso])
    print('Total usage: ' + str(total_usage))

    for price in prices:
        if price['datetime'] in eso.keys():
            row = eso[price['datetime']]
            row['price'] = price['price_np'] / 1000
            row['cost'] = row['price'] * row['usage']
            
    hour_count = len(eso)
    period_average = sum([eso[date]['price'] for date in eso]) / hour_count

    print("Average price: " + str(period_average))

    hourly_cost = sum([eso[date]['cost'] for date in eso])
    monthly_cost = total_usage * period_average

    print('Hourly cost:  ' + str(hourly_cost))
    print('Monthly cost: ' + str(monthly_cost))

