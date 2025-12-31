#!/usr/bin/env python3
"""
Order Processing Worker
Xử lý orders từ queue "order_processing"
"""
import pika
import json
import time
import sys
import os
from datetime import datetime

# Add shared folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from shared.config import RABBITMQ_HOST, ORDER_QUEUE
from shared.db import get_db_connection

def connect_rabbitmq():
  connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
  )
  return connection, connection.channel()

def process_order(order_data):
    """
    Xử lý order (simulate các bước xử lý)
    """
    order_id = order_data.get('order_id')
    customer_name = order_data.get('customer_name')
    customer_email = order_data.get('customer_email')
    product_name = order_data.get('product_name')
    total_price = order_data.get('total_price')
    
    print(f"  Processing order #{order_id} for {customer_name}")
    
    # Simulate các bước xử lý
    steps = [
        ('Validating inventory', 0.5),
        ('Calculating shipping', 0.3),
        ('Sending confirmation email', 1.0),
        ('Updating analytics', 0.2),
    ]
    
    for step_name, step_time in steps:
        print(f"    - {step_name}...")
        time.sleep(step_time)
    
    # Update order status trong database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE orders SET status = ? WHERE id = ?',
            ('COMPLETED', order_id)
        )
        conn.commit()
        conn.close()
        print(f"  [OK] Order #{order_id} completed successfully")
    except Exception as e:
        print(f"  [ERROR] Failed to update order status: {e}")
    
    return True

def on_message(channel, method, properties, body):
    """Callback khi nhận message"""
    try:
        order_data = json.loads(body)
        order_id = order_data.get('order_id', 'Unknown')
        
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Received order: #{order_id}")
        print(f"  Customer: {order_data.get('customer_name')}")
        print(f"  Product: {order_data.get('product_name')}")
        print(f"  Total: ${order_data.get('total_price', 0):.2f}")
        
        # Xử lý order
        success = process_order(order_data)
        
        if success:
            channel.basic_ack(delivery_tag=method.delivery_tag)
            print(f"  [OK] Acknowledged order #{order_id}")
        else:
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            print(f"  [ERROR] Failed to process order #{order_id}")
            
    except Exception as e:
        print(f"  [ERROR] Error processing message: {e}")
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def main():
    """Main function"""
    print("=" * 60)
    print("Order Processing Worker")
    print("=" * 60)
    
    try:
        connection, channel = connect_rabbitmq()
        print("[OK] Connected to RabbitMQ")
    except Exception as e:
        print(f"[ERROR] Failed to connect to RabbitMQ: {e}")
        print("\nMake sure RabbitMQ is running:")
        print("  docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management")
        return
    
    # Declare queue
    channel.queue_declare(queue=ORDER_QUEUE, durable=True)
    channel.basic_qos(prefetch_count=1)
    
    print(f"\nWaiting for orders in queue '{ORDER_QUEUE}'...")
    print("Press CTRL+C to exit\n")
    
    channel.basic_consume(
        queue=ORDER_QUEUE,
        on_message_callback=on_message
    )
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n\nStopping worker...")
        channel.stop_consuming()
        connection.close()
        print("Connection closed")

if __name__ == '__main__':
    main()

