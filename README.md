# crontab config
```
45 * * * * /var/www/nordpool/.venv/bin/python3 /var/www/nordpool/crawler/crawler.py
@hourly /var/www/nordpool/.venv/bin/python3 /var/www/nordpool/plugs/update.py
```
