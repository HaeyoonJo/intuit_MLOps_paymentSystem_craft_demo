import json
import random

def process_payment(body):
    payment_info = json.loads(body)
    payment_id = payment_info['payment_id']
    random_num = random.random()

    if random_num < 0.7:
        print(f"Payment {payment_id} approved. Random num: {random_num}", flush=True)
        # Further processing for approved payment
    else:
        print(f"Payment {payment_id} declined. Random num: {random_num}", flush=True)
        # Further processing for declined payment