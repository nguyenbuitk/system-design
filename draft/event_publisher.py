#!/usr/bin/env python3
"""
Event Publisher
Publish events vào topic exchange
"""
import pika
import json
import sys
import os
from datetime import datetime

# Add parent to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from shared.config import EXCHANGE_NAME, EXCHANGE_TYPE
from shared.rabbitmq_utils import get_rabbitmq_connection, setup_exchange

def publish_event(channel, routing_key, event_data):
    """Publish event vào topic exchange"""
    message = json.dumps(event_data)
    
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=routing_key,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make message persistent
        )
    )
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Published: {routing_key}")
    print(f"  Data: {event_data}")

def main():
    """Main function - Publish sample events"""
    print("=" * 60)
    print("Event Publisher - Pub/Sub Demo")
    print("=" * 60)
    
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        setup_exchange(channel)
        print("[OK] Connected to RabbitMQ")
        print(f"[OK] Exchange '{EXCHANGE_NAME}' ready")
    except Exception as e:
        print(f"[ERROR] Failed to connect to RabbitMQ: {e}")
        print("\nMake sure RabbitMQ is running:")
        print("  docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management")
        return
    
    print("\nPublishing events...")
    print("-" * 60)
    
    # User events
    publish_event(channel, 'user.created', {
        'event_type': 'user.created',
        'user_id': 1,
        'email': 'user1@example.com',
        'name': 'John Doe',
        'timestamp': datetime.now().isoformat()
    })
    
    publish_event(channel, 'user.login', {
        'event_type': 'user.login',
        'user_id': 1,
        'ip_address': '192.168.1.100',
        'timestamp': datetime.now().isoformat()
    })
    
    # Order events
    publish_event(channel, 'order.created', {
        'event_type': 'order.created',
        'order_id': 101,
        'user_id': 1,
        'total': 99.99,
        'items': ['Product A', 'Product B'],
        'timestamp': datetime.now().isoformat()
    })
    
    # Payment events
    publish_event(channel, 'payment.completed', {
        'event_type': 'payment.completed',
        'payment_id': 201,
        'order_id': 101,
        'amount': 99.99,
        'method': 'credit_card',
        'timestamp': datetime.now().isoformat()
    })
    
    publish_event(channel, 'payment.failed', {
        'event_type': 'payment.failed',
        'payment_id': 202,
        'order_id': 102,
        'amount': 49.99,
        'reason': 'Insufficient funds',
        'timestamp': datetime.now().isoformat()
    })
    
    print("-" * 60)
    print("[OK] All events published!")
    print("\nCheck subscribers terminals to see events being received")
    
    connection.close()

if __name__ == '__main__':
    main()