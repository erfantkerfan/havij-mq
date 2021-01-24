import sys
import threading
from threading import Thread

import requests
from pymongo import MongoClient
from tqdm import tqdm

SIMULTANEOUS_THREADS = 100
THREADING = False
SERVER_URL = 'http://192.168.4.3:500'
SERVER_MONGO = '192.168.4.3'
MONGO_DB = '3a_new'

client = MongoClient(SERVER_MONGO)
db = client.get_database(MONGO_DB)
collection = db.get_collection('logs')
# cursor = collection.find({}).limit(500)
cursor = collection.find({}, no_cursor_timeout=True)

headers = {
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
    temp_header = headers
    temp_header['Authorization'] = 'Bearer ' + message['token']
    temp_data = message['parameter']
    temp_data['log_id'] = message['_id']
    temp_data['created_at'] = message['created_at']
    response = requests.request(message['method'], SERVER_URL + message['url'], headers=temp_header, data=temp_data)
    status_code = response.status_code
    STATUS_CODES.setdefault(status_code, 0)
    STATUS_CODES[status_code] += 1


threads = []
for message in tqdm(cursor, desc='making requests ', unit=' request', ncols=250):
    try:
        if THREADING:
            while threading.activeCount() > SIMULTANEOUS_THREADS:
                pass
            threads = [t for t in threads if t.is_alive()]
            threads.append(Thread(target=send_request, args=(message,)))
            threads[-1].start()
        else:
            send_request(message)
    except KeyboardInterrupt:
        sys.exit()
    except:
        print('thread failed')
cursor.close()
while any([t.is_alive for t in threads]):
    threads = [t for t in threads if t.is_alive()]

print(STATUS_CODES)
