from zoneinfo import ZoneInfo

def add_price(prices):
    for price in prices:
        price['price'] = _add_taxes(price['datetime'], price['price_np'])
    return prices

def _add_taxes(datetime, price):
    datetime = datetime.astimezone(ZoneInfo('Etc/GMT+3')) # LT summer time zone
    hour = datetime.time().hour
    weekday = datetime.weekday()

    price = price / 1000 # kWh
    price *= 1.21 # PVM
    price += 0.02821 # Tiekimo paslauga
    price += -0.00944 # VIAP
    price += 0.00006 # Skirstymo dedamoji

    if (hour >= 0 or hour < 8) or weekday >= 6: # 24-08 or weekends
        price += 0.04719 # Persiuntimo paslauga naktis
    else:
        price += 0.07865 # Persiuntimo paslauga diena
    price *= 100 # ct

    return price
