"""
Shared RabbitMQ utilities for Pub-Sub
"""
import pika
import sys
import os

# Add parent to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from shared.config import RABBITMQ_HOST, EXCHANGE_NAME, EXCHANGE_TYPE

def get_rabbitmq_connection():
    """Lấy RabbitMQ connection"""
    return pika.BlockingConnection(
        pika.ConnectionParameters(RABBITMQ_HOST)
    )

def setup_exchange(channel):
    """Setup topic exchange"""
    channel.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type=EXCHANGE_TYPE,
        durable=True
    )

