from risk_analysis import process_payment

def callback(ch, method, properties, body):
    print(f'Received message: {body}', flush=True)
    process_payment(body)

def start_consuming(channel):
    channel.basic_consume(queue='my_queue', on_message_callback=callback, auto_ack=True)
    print('Waiting for messages...')
    channel.start_consuming()