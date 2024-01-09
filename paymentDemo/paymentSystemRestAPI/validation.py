from marshmallow import Schema, fields, ValidationError

# Class:
#   Validate these fields are in the payload.
# Required fields
#   amount: Number
#   currency: String 
#   userId: String
#   payeeId: String
#   paymentMethodId: String

class PaymentSchema(Schema):
    amount = fields.Number(required=True)
    currency = fields.Str(required=True)
    userId = fields.Str(required=True)
    payeeId = fields.Str(required=True)
    paymentMethodId = fields.Str(required=True)

def validate_payment_data(payment_data):
    payment_schema = PaymentSchema()
    return payment_schema.load(payment_data)