import json, os, requests, datetime

HISTORY_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'history.json')

API_URL = 'https://www.eso.lt/web/atjungimai-planiniai-neplaniniai/mapdata?fg=1&fk=0&fn=1&fp=1'
TIMEOUT = 60

def _main():
    response = requests.get(API_URL, timeout=TIMEOUT)
    if response.status_code != 200:
        return

    temp = response.json()
    if not temp['success'] or len(temp['data']) == 0:
        return

    history = {}
    if os.path.isfile(HISTORY_PATH):
        with open(HISTORY_PATH, 'r') as read:
            history = json.load(read)

    now = datetime.datetime.now(datetime.UTC).strftime('%y-%m-%d %H')
    for row in temp['data']:
        if not row['pas_id'] in history.keys():
            history[row['pas_id']] = {}
        history[row['pas_id']][now] = row['type']

    with open(HISTORY_PATH, 'w') as write:
        json.dump(history, write)

if __name__ == "__main__":
    _main()
