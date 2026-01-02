import pika
import json
import time
from datetime import datetime

def connect_rabbitmq():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')
    )
    return connection, connection.channel()

def process_task(task_data):
    task_id = task_data.get('task_id')
    description = task_data.get('description')
    task_type = task_data.get('type', 'unknown')
    
    print(f"  Processing: {description}")
    
    processing_times = {
    'image_processing': 1,
    'email': 0.5,
    'report': 1
    }
    
  processing_time = processing_times.get(task_type, 1)
    time.sleep(processing_time)
  print(f"  [OK] Completed: {task_id}")
    return True

def on_message(channel, method, properties, body):
    """
    Callback function called when a message is received.
    """
    try:
        task_data = json.loads(body)
        task_id = task_data.get('task_id', 'Unknown')
        
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Received: {task_id}")
        print(f"  Type: {task_data.get('type', 'unknown')}")
        
        success = process_task(task_data)
        
        if success:
      # Acknowledge message (tell RabbitMQ the message was process successfully)
            channel.basic_ack(delivery_tag=method.delivery_tag)
      print(f"  [OK] Acknowledged: {task_id}")
        else:
      channel.basic_nack(delivery_tag=method.delivery_tag)
      print(f"  [ERROR] Failed: {task_id} (requeued)")
    #if success:
    #  channel.basic_ack(delivery_tag=)
    
    except Exception as e:
    print(f"  [ERROR] Error processing message: {e}")
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def main():
  """Main function to start consuming message."""
    print("=" * 60)
    print("RabbitMQ Simple Queue - Consumer")
    print("=" * 60)
    
    try:
        connection, channel = connect_rabbitmq()
    print(f"[OK] Connnected to RabbitMQ: {connection}") 
    print(f"[OK] Channel: {channel}")
    except Exception as e:
    print(f"[ERROR] Failed to connect to RabbitMQ: {e}")
        return
    
  queue_name = 'queue_test'
    channel.queue_declare(queue=queue_name, durable=True)
  # prefetch_count = 1 means don't give more than 1 message to a worker at a time
    channel.basic_qos(prefetch_count=1)
    
  print(f"\nWaiting for messages in queue '{queue_name}'...")
    print("Press CTRL+C to exit\n")
    
  # Setup consumer
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=on_message
    )
    
    try:
    # Start consuming (this blocks until interupted)
    print(f"Starting consumming message queue: {queue_name}...")
        channel.start_consuming()
    except KeyboardInterrupt:
    print("\n\nStop consumer...")
        channel.stop_consuming()
        connection.close()
    print("Connection closed")

if __name__ == '__main__':
    main()