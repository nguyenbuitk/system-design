"""
Shared RabbitMQ utilities
"""
import pika
import json
import sys
import os

# Import config
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
try:
    from shared.config import RABBITMQ_HOST
except ImportError:
    # Fallback if running as script
    RABBITMQ_HOST = 'localhost'

def get_rabbitmq_connection():
    """Lấy RabbitMQ connection"""
    return pika.BlockingConnection(
        pika.ConnectionParameters(RABBITMQ_HOST)
    )

def send_to_queue(queue_name, message_data):
    """Gửi message vào queue"""
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        
        # Declare queue (durable=True để survive broker restart)
        channel.queue_declare(queue=queue_name, durable=True)
        
        # Publish message
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

