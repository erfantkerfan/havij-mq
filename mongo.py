import sys
import threading
from threading import Thread

import requests
from pymongo import MongoClient
from tqdm import tqdm

client = MongoClient('127.0.0.1')
db = client.get_database('3a_new')
collection = db.get_collection('logs')
# cursor = collection.find({}).limit(500)
cursor = collection.find({}, no_cursor_timeout=True)

HEADERS = {
    'Accept': 'application/json',
    'Cookie': 'nocache=1',
    'Accept-Encoding': 'utf-8'
}

STATUS_CODES = dict()


def print_log():
    threading.Timer(10.0, print_log).start()
    print(STATUS_CODES)


print_log()


def send_request(message):
    pass
    temp = HEADERS
    temp['Authorization'] = 'Bearer ' + message['token']
    if message['method'] == 'GET':
        response = requests.request(message['method'], 'http://192.168.4.3:500' + message['url'], headers=temp,
                                    params=message)
    else:
        response = requests.request(message['method'], 'http://192.168.4.3:500' + message['url'], headers=temp,
                                    data=message)
    status_code = response.status_code
    STATUS_CODES.setdefault(status_code, 0)
    STATUS_CODES[status_code] += 1

    # if status_code != 200:
    #     print(status_code)
    #     print(response.text)


threads = []
for message in tqdm(cursor, desc='making requests ', unit=' request', ncols=250):
    try:
        # while threading.activeCount() > 100:
        #     pass
        # threads = [t for t in threads if t.is_alive()]
        # threads.append(Thread(target=send_request, args=(message,)))
        # threads[-1].start()
        send_request(message)
    except KeyboardInterrupt:
        sys.exit()
    except:
        print('thread failed')

while any([t.is_alive for t in threads]):
    threads = [t for t in threads if t.is_alive()]

print(STATUS_CODES)
