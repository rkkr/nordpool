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
    price += 0.0001 # Tiekimo paslauga
    price += -0.0004719 # VIAP
    price += 0.00108053 # Skirstymo dedamoji

    if (hour >= 0 and hour < 8) or weekday >= 5: # 24-08 or weekends
        price += 0.05324 # Persiuntimo paslauga naktis
    else:
        price += 0.09801 # Persiuntimo paslauga diena
    price *= 100 # ct

    return price
