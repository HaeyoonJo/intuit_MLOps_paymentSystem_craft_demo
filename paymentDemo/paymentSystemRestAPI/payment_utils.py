import uuid
import requests

# Payment ID Generation: This is a utility function that generating paymentId to return to client
def generate_payment_id():
    return str(uuid.uuid4())

# Payment Capture: Skipped function
def request_payment_capture(payment_id):
    capture_url = f'http://localhost:5000/payments/{payment_id}/capture'
    return requests.put(capture_url)