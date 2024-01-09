from rabbitmq_utils import create_connection, setup_channel
from risk_engine_handler import start_consuming

if __name__ == '__main__':
    connection = create_connection()
    channel = setup_channel(connection)
    start_consuming(channel)