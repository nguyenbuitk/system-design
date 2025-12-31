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
        
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] [LOG] {routing_key}")
        print(f"  {json.dumps(event_data, indent=2)}")
        
        channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"  [ERROR] {e}")
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def main():
    print("Log Subscriber")
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
    
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key='#')
    
    print("Subscribed to: # (all events)")
    print("Waiting for events...\n")
    
    channel.basic_consume(queue=queue_name, on_message_callback=on_message)
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        connection.close()

if __name__ == '__main__':
    main()

