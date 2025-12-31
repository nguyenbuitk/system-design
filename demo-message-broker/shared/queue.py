"""
Shared RabbitMQ utilities
"""
import pika
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from shared.config import RABBITMQ_HOST

def get_rabbitmq_connection():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(f'{RABBITMQ_HOST}')
    )
    return connection, connection.channel()

def send_to_queue(queue_name, message_data):
    try:
        connection, channel = get_rabbitmq_connection()
        channel = connection.channel()
        
        channel.queue_declare(queue=queue_name, durable=True)
        
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message_data),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )
        
        connection.close()
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send to queue: {e}")
        return False
