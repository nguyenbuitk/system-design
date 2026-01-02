import pika
import json
import sys
import os
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from shared.config import EXCHANGE_NAME
from shared.rabbitmq_utils import get_rabbitmq_connection, setup_exchange

def on_message(channel, method, properties, body):
    try:
        event_data = json.loads(body)
        routing_key = method.routing_key
        
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] [EMAIL] {routing_key}")
        
        if routing_key == 'user.created':
            print(f"  Sending welcome email to {event_data.get('email')}")
        elif routing_key == 'order.created':
            print(f"  Sending order confirmation (Order #{event_data.get('order_id')})")
        elif routing_key == 'payment.completed':
            print(f"  Sending payment receipt (${event_data.get('amount')})")
        
        channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"  [ERROR] {e}")
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def main():
    print("Email Subscriber")
    print("=" * 60)
    
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        setup_exchange(channel)
        print("[OK] Connected to RabbitMQ")
    except Exception as e:
        print(f"[ERROR] {e}")
        return
    
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    
    for routing_key in ['user.*', 'order.created', 'payment.completed']:
        channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key=routing_key)
    
    print("Subscribed to: user.*, order.created, payment.completed")
    print("Waiting for events...\n")
    
    channel.basic_consume(queue=queue_name, on_message_callback=on_message)
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        connection.close()

if __name__ == '__main__':
    main()

