# crontab config
```
45 * * * * /var/www/nordpool/.venv/bin/python3 /var/www/nordpool/crawler/crawler.py
@hourly /var/www/nordpool/.venv/bin/python3 /var/www/nordpool/plugs/update.py
```

# apache site config
```
ScriptAlias /nordpool /var/www/nordpool/http/index.py
<Directory /var/www/nordpool/http>
        AllowOverride None
        Order allow,deny
        Allow from all
        AddHandler mod_python .py
        PythonHandler index
        PythonDebug On
</Directory>
```

