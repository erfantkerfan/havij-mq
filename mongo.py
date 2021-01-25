import json
import sys
import threading
from threading import Thread

import requests
from bson import json_util
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
# cursor = collection.find({'_id': ObjectId("6003c31ebf8cdd46074c8314")})
cursor = collection.find({'url': {'$regex': 'temp-exam', '$options': 'i'}, 'method': 'POST'})

headers = {
    'Accept': 'application/json',
    'Cookie': 'nocache=1',
    'Accept-Encoding': 'utf-8',
    'Content-Type': 'application/json',
}
STATUS_CODES = dict()


def print_log():
    if logger:
        threading.Timer(5.0, print_log).start()
        print(STATUS_CODES)


logger = True
print_log()


def parse_json(data):
    return json.loads(json_util.dumps(data))


def send_request(message):
    temp_header = headers
    temp_header['Authorization'] = 'Bearer ' + message['token']
    temp_data = parse_json(message['parameter'])
    temp_data['log_id'] = str(message['_id'])
    temp_data['created_at'] = message['created_at'].strftime('%Y-%m-%d %H:%M:%S')
    response = requests.request(message['method'], SERVER_URL + message['url'], headers=temp_header, json=temp_data)
    status_code = response.status_code
    STATUS_CODES.setdefault(status_code, 0)
    STATUS_CODES[status_code] += 1


threads = []
for message in tqdm(cursor, desc='making requests ', unit=' request', ncols=250):
    try:
        if message['method'] == 'POST' and 'temp-exam' in message['url']:
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
    except Exception as error:
        print('thread failed ' + str(error))
cursor.close()
while any([t.is_alive for t in threads]):
    threads = [t for t in threads if t.is_alive()]

logger = False
print(STATUS_CODES)
