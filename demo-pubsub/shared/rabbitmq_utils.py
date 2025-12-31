import pika
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from shared.config import RABBITMQ_HOST, EXCHANGE_NAME, EXCHANGE_TYPE

def get_rabbitmq_connection():
    return pika.BlockingConnection(
        pika.ConnectionParameters(RABBITMQ_HOST)
    )

def setup_exchange(channel):
    channel.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type=EXCHANGE_TYPE,
        durable=True
    )