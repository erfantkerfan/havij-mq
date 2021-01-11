import json

import pika
from tqdm import tqdm

message = {
    'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiNjU3M2I5ZDA0YjljNDA0NjQ4ZjUwMGJkZjYzZTNlNTU3NTk0ZjU4OWRjN2JkZTcwNWE1MjYwNDQ0YmI3MTg1MmRkZWNkODEzNTE2NWMyNGIiLCJpYXQiOjE2MTAyNzE4ODYsIm5iZiI6MTYxMDI3MTg4NiwiZXhwIjoxNjQxODA3ODg2LCJzdWIiOiIzODkyNzAiLCJzY29wZXMiOltdfQ.NxudRynsXYSwWRTxUsUXJbXgB5cLC0LJYMWIzuaq0BJsAXpp4yOpJ7e0tfkNwS8q-UcFPq5BW3CnffpPLsF8wWhveUqBsYI_Ex5mGl5tc65HojhDdt2_kCewo30GRXmq0JNfewV-OG2xC1oBaZU1m2JUBHLxTxI6rltZ0WnK6y5mHjdU7isXiZqOStrftIgWKbBxFWzmPqq8-ZlRIkpsAYuseZdybh0w1XCKq-EywbP9j3ARovz8w4seuAj8OKsfUEShueA4Lhur8grfPfiDfzmA-56xM3F8AuOrfpRVU0FRMHQ93JchYqdLwS7aA9mdT2D13ixr-IgrcYoeJtzYAXZKVKD_loaGr0HHi5DRJDQfs8kdu8dgtrKpFFO4GWEkzd1qY_zA2RcO2cLB_lFPjXY7E8JNwxGHyrkKKbXJcaaKMKVT2CiHb-wZUPnos-f74X7l2dbXzHThNvvZ0facfJawpSfbAdJn-0X5I1nmCGO6Q0xjxQLMBy7j0lf3wJ8UZi-l1eDDyM_6cWrHMhVH8lOMc1mj8eMTF9y0k2o7mJc7pZW49gPo8Eh2ky5uWgIAEH-kZgN8voXksExq3kBqH1IlSB6l7O-VxQ7jN8jzRJG2xS6HPPFPo6FDQYsTcTfrw_RgheONfRaJ7T8geJ_hit7JugH92veJAUaMRHOKtPQ',
    'url': '/exam?id=5ffabb4e0d7c702a56046835',
    'method': 'get',
    'jigil': 'fingil',
    'nini': 'mimi',
}
queue_name = 'test'
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue=queue_name)

reqs = 500
bar = tqdm(total=reqs, desc='making requests ', unit=' request', ncols=250)
for i in range(reqs):
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))
    bar.update(1)
    # print(i)
bar.close()
connection.close()
