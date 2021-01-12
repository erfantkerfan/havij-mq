import datetime
import json
import logging
import os
import sys
import threading
from datetime import date
from threading import Thread

import pika
import requests
from dotenv import load_dotenv


def main():
    config()
    balance()


def config():
    global CONFIG, HEADERS
    load_dotenv()
    log_levels = ['--DEBUG', '--INFO', '--WARNING', '--ERROR', '--CRITICAL']
    USAGE = '''
RabbitMQ consumer APP

--help          for help
--[level]       for log level {levels}'''.format(length='multi-line', levels=log_levels)

    HEADERS = {
        'Accept': 'application/json',
        'Cookie': 'nocache=1',
        'Accept-Encoding': 'utf-8'
    }

    opts = [opt for opt in sys.argv[1:] if opt.startswith("--")]
    if "--help" in opts:
        print(USAGE)
        exit(0)
    try:
        log_level = (str(list(set(log_levels) & set(opts))[0])).replace('--', '')
    except IndexError:
        log_level = (str(log_levels[-1])).replace('--', '')

    today = date.today()
    log_file = str(today) + '.log'
    log_format = '%(levelname)s %(asctime)s - %(message)s'
    logging.basicConfig(filename=log_file,
                        format=log_format,
                        level=getattr(logging, log_level))

    CONFIG = {
        'SIMULTANEOUS_THREADS': int(os.getenv("SIMULTANEOUS_THREADS", 20)),

        'RabbitMQServer': os.getenv("RabbitMQServer", 'localhost'),
        'RabbitMQPort': os.getenv("RabbitMQPort", '5672'),
        'RabbitMQQOS': int(os.getenv("RabbitMQQOS", 10)),
        'RabbitMQQueue': os.getenv("RabbitMQQueue", 'test'),

        'LumenSchema': os.getenv("LumenSchema", 'http'),
        'LumenServer': os.getenv("LumenServer", 'localhost'),
        'LumenPort': int(os.getenv("LumenPort", 80)),
    }


def balance():
    try:
        threads = []
        while threading.activeCount() > CONFIG['SIMULTANEOUS_THREADS']:
            pass
        threads = [t for t in threads if t.is_alive()]

        threads.append(Thread(target=connection))
        threads[-1].start()
    except KeyboardInterrupt:
        exit()


def connection():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=CONFIG['RabbitMQServer'], heartbeat=60))
        channel = connection.channel()
        channel.queue_declare(queue=CONFIG['RabbitMQQueue'])
        channel.basic_qos(prefetch_count=CONFIG['RabbitMQQOS'])
        channel.basic_consume(queue=CONFIG['RabbitMQQueue'], on_message_callback=send_request, auto_ack=True)
        try:
            logging.info('thread started listening consuming')
            channel.start_consuming()
        except:
            logging.critical('thread consumption fialed')
            channel.stop_consuming()
    except:
        logging.critical('connection to MQ failed')

    connection.close()


def send_request(ch, method, properties, body):
    start = datetime.datetime.now()
    message = json.loads(body)
    HEADERS['Authorization'] = message['token']
    payload = message
    response = requests.request(message['method'], CONFIG['LumenSchema'] + CONFIG['LumenServer'] + message['url'],
                                headers=HEADERS, data=payload)
    try:
        status_code = response.status_code
        if status_code != 200:
            logging.critical('request failed')
        data = json.loads(response.content)
        logging.debug(status_code)
        logging.debug(data)
    except:
        logging.critical('request failed')
    # send req if failed push back to qeue
    # queue_name = to
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    # channel = connection.channel()
    # channel.queue_declare(queue=queue_name)
    # channel.basic_publish(exchange='',
    #                       routing_key=queue_name,
    #                       body=json.dumps(message))
    # connection.close()
    #
    # logging.basicConfig(filename='log.txt',
    #                     filemode='a',
    #                     format='%(asctime)s ---> %(message)s',
    #                     datefmt='%H:%M:%S',
    #                     level=logging.CRITICAL)

    end = datetime.datetime.now()
    elapsed = end - start
    logging.debug('time spend on a single request: ' + str(elapsed.microseconds))


main()
