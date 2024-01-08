import pika

def create_connection():
    for i in range(5):  # Retry up to 5 times
        try:
            credentials = pika.PlainCredentials('admin', 'admin')
            connection = pika.BlockingConnection(
                pika.ConnectionParameters('rabbitmq', credentials=credentials, heartbeat=60)
            )
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Connection attempt {i+1}/5 failed: {e}")
            time.sleep(10)  # Wait for 10 seconds before retrying
    raise Exception("Failed to connect to RabbitMQ after several attempts")


connection = create_connection()
channel = connection.channel()
channel.queue_declare(queue='my_queue')


def callback(ch, method, properties, body):
    print(f'Received message: {body}', flush=True)

channel.basic_consume(queue='my_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages...')
channel.start_consuming()
