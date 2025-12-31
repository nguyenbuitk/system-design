#!/usr/bin/env python3
"""
RabbitMQ Simple Queue - Producer
Sends tasks to a message queue for processing.
"""

import pika
import json
import time
from datetime import datetime


def connect_rabbitmq():
    """Establish connection to RabbitMQ server."""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')
    )
    return connection, connection.channel()


def send_task(channel, queue_name, task_data):
    """Send a task to the queue."""
    # Declare queue (create if doesn't exist)
    # durable=True makes the queue survive broker restarts
    channel.queue_declare(queue=queue_name, durable=True)
    
    # Convert task data to JSON
    message = json.dumps(task_data)
    
    # Publish message
    # delivery_mode=2 makes message persistent
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make message persistent
        )
    )
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Sent: {task_data['task_id']} - {task_data['description']}")


def main():
    """Main function to send multiple tasks."""
    print("=" * 60)
    print("RabbitMQ Simple Queue - Producer")
    print("=" * 60)
    
    # Connect to RabbitMQ
    try:
        connection, channel = connect_rabbitmq()
        print("[OK] Connected to RabbitMQ")
    except Exception as e:
        print(f"[ERROR] Failed to connect to RabbitMQ: {e}")
        print("\nMake sure RabbitMQ is running:")
        print("  docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management")
        return
    
    queue_name = 'queue_test'
    
    # Define tasks to send (5 tasks for quick demo)
    tasks = [
        {'task_id': 'T001', 'description': 'Process image: photo1.jpg', 'type': 'image_processing'},
        {'task_id': 'T002', 'description': 'Send email: welcome@example.com', 'type': 'email'},
        {'task_id': 'T003', 'description': 'Process image: photo2.jpg', 'type': 'image_processing'},
        {'task_id': 'T004', 'description': 'Generate report: sales_q1', 'type': 'report'},
        {'task_id': 'T005', 'description': 'Send email: invoice@example.com', 'type': 'email'},
    ]
    
    print(f"\nSending {len(tasks)} tasks to queue '{queue_name}'...")
    print("-" * 60)
    
    # Send all tasks
    for task in tasks:
        send_task(channel, queue_name, task)
        time.sleep(0.2)  # Small delay between messages
    
    print("-" * 60)
    print(f"[OK] All {len(tasks)} tasks sent successfully!")
    print("\nNext: Run consumer.py in another terminal to process tasks")
    
    # Close connection
    connection.close()


if __name__ == '__main__':
    main()