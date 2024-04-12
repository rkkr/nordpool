from datetime import datetime, timedelta

def add_price(prices):
    for price in prices:
        price['price'] = _add_taxes(price['datetime'], price['price_np'])
    return prices

def _add_taxes(timestamp: datetime, price: float):
    timestamp = timestamp + timedelta(hours=3) # LT summer time zone
    hour = timestamp.time().hour
    weekday = timestamp.weekday()

    price = price / 1000 # kWh
    price *= 1.21 # PVM
    price += 0.02226 # Tiekimo paslauga
    price += 0.0 # VIAP
    price += 0.00054 # Skirstymo dedamoji

    if (hour >= 0 and hour < 8) or weekday >= 6: # 24-08 or weekends
        price += 0.06050 # Persiuntimo paslauga naktis
    else:
        price += 0.10285 # Persiuntimo paslauga diena
    price *= 100 # ct

    return price
