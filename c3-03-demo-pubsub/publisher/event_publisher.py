import pika
import json
import sys
import os
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from shared.config import EXCHANGE_NAME
from shared.rabbitmq_utils import get_rabbitmq_connection, setup_exchange

def publish_event(channel, routing_key, event_data):
    message = json.dumps(event_data)
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=routing_key,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Published: {routing_key}")

def main():
    print("Event Publisher - Pub/Sub Demo")
    print("=" * 60)
    
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        setup_exchange(channel)
        print("[OK] Connected to RabbitMQ")
    except Exception as e:
        print(f"[ERROR] Failed to connect: {e}")
        return
    
    events = [
        ('user.created', {'event_type': 'user.created', 'user_id': 1, 'email': 'user1@example.com'}),
        ('user.login', {'event_type': 'user.login', 'user_id': 1, 'ip_address': '192.168.1.100'}),
        ('order.created', {'event_type': 'order.created', 'order_id': 101, 'user_id': 1, 'total': 99.99}),
        ('payment.completed', {'event_type': 'payment.completed', 'payment_id': 201, 'order_id': 101, 'amount': 99.99}),
        ('payment.failed', {'event_type': 'payment.failed', 'payment_id': 202, 'order_id': 102, 'amount': 49.99, 'reason': 'Insufficient funds'}),
    ]
    
    for routing_key, data in events:
        data['timestamp'] = datetime.now().isoformat()
        publish_event(channel, routing_key, data)
    
    print("[OK] All events published!")
    connection.close()

if __name__ == "__main__":
    main()