import json
import os

import pika
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()
CONFIG = {
    'RabbitMQServer': os.getenv("RabbitMQServer", 'localhost'),
    'RabbitMQPort': os.getenv("RabbitMQPort", '5672'),
    'RabbitMQQueue': os.getenv("RabbitMQQueue", 'test'),

    'NginxProxyPort': int(os.getenv("NginxProxyPort", '8080')),
}

connection = pika.BlockingConnection(pika.ConnectionParameters(host=CONFIG['RabbitMQServer'], heartbeat=0))
channel = connection.channel()
channel.queue_declare(queue=CONFIG['RabbitMQQueue'])


async def handle(request):
    data = await request.post()
    response = dict(data)
    try:
        jsons = await request.json()
        response.update(jsons)
    except:
        pass
    response.update({
        'method': request.method,
        'url': request.path,
        'token': request.headers['Authorization'],
    })
    channel.basic_publish(exchange='',
                          routing_key=CONFIG['RabbitMQQueue'],
                          body=json.dumps(response))
    return web.json_response(response)


app = web.Application()
app.router.add_route('GET', '/{tail:.*}', handle)
app.router.add_route('POST', '/{tail:.*}', handle)
app.router.add_route('PUT', '/{tail:.*}', handle)
app.router.add_route('DELETE', '/{tail:.*}', handle)

if __name__ == '__main__':
    web.run_app(app, port=CONFIG['NginxProxyPort'])
    connection.close()
