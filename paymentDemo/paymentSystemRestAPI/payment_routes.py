from flask import Blueprint, request, jsonify
import json
import marshmallow

from validation import validate_payment_data
from payment_utils import generate_payment_id
from rabbitmq_utils import get_rabbitmq_channel

payment_routes = Blueprint('payment_routes', __name__)

@payment_routes.route('/payments', methods=['POST'])
def receive_payment():
    """Receives payment information and publishes it to the 'my_queue' queue."""
    try:
        data = request.json
        validated_data = validate_payment_data(data)
        payment_id = generate_payment_id()

        message = json.dumps({
            'payment_data': validated_data,
            'payment_id': payment_id
        })

        with get_rabbitmq_channel() as channel:    
            channel.queue_declare(queue='my_queue')
            channel.basic_publish(exchange='', routing_key='my_queue', body=message)

        response = jsonify({
            'statusCode': 201,
            'status': 'Payment information published to queue',
            'paymentId': payment_id
        })
        return response, 201

    except marshmallow.ValidationError as e:
        return jsonify({
            'statusCode': 400,
            'status': 'Bad Request. Failed to validate requests',
            'error': str(e)
        }), 400

    except Exception as e:
        return jsonify({
            'statusCode': 500,
            'status': 'Error processing payment',
            'error': str(e)
        }), 500