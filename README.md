# payment System Craft Demo
This Payment System demo repo provides brief workflow operates on AWS along with deployed Risk Engine application as well as details on Wiki document.

## Jump to:
- [Payment System REST APIs](#REST-API-guidance)
- [Payload attributes](#Payload-attributes)
- [Getting Started](#Getting-Started)
- [Getting Help](#Getting-Help)
- [More guidance](#More-guidance)

# REST API guidance
The Payment processing platform provides several RESTful APIs to create, capture and retrieve payments.

## API Authentication
All APIs require authorization using an API key or JWT token. The token should be passed in the Authorization header:

```
Authorization: <api_key or JWT token> 
```

## Create payment
To create a new payment, send `POST` request to the `/payments` endpoint.

- Request
See the attribute details in the [Payload attributes](#Payload-attributes) section below.
```
POST /payments
Authorization: Bearer <jwt-token>
{
  "amount": 70.5,
  "currency": "USD",
  "userId": "e8af92bd-1910-421e-8de0-cb3dcf9bf44d",
  "payeeId": "4c3e304e-ce79-4f53-bb26-4e198e6c780a",
  "paymentMethodId": "8e28af1b-a3a0-43a9-96cc-57d66dd68294"
}
```

The body should contain payment details like `amount`, `currency`, `userId`, `payeeId` and `paymentMethodId`. This will be validated against the PaymentSchema before payment creation.

- Response

Status: 201 Created
Description: The request was successfully fulfilled and resulted in one created
Body: See below
```
Status: 201 OK
{
  "Result": "Success",
  "PaymentId": "5565f337-c901-458c-bab8-20fcf12ba573"
}
```

The response contains the `Result`, `PaymentId` and `status` indicating the payment is successfully completed. An optional addtiributes can also be returned in the near future if needed.



# Payload attributes

The payment creation request payload contains the following attributes:

### amount

- Type: `number`

- Description: Amount to pay

### currency 

- Type: `string`

- Description: Payment currency (e.g. USD, EUR)

### userId

- Type: `string` 

- Description: Paying user unique identifier (GUID)

### payeeId

- Type: `string`

- Description: Payee user unique identifier (GUID) 

### paymentMethodId

- Type: `string` 

- Description: Payment method unique identifier (GUID)

## Sample Request
This example request payload:
- Amount to pay of 100
- Currency is USD
- userId, payeeId, paymentMethodId provided as GUID strings

The payload is validated against the PaymentSchema before creating the payment

```json
{
  "amount": 100,
  "currency": "USD",
  "userId": "817612a1-97c0-4ea2-9f22-f1bc9ab1d074",
  "payeeId": "c4e83104-b9e7-4bd6-a290-8122ecd9914a",
  "paymentMethodId": "2adffd95-5dcf-4a70-a709-3eae2fcf00f2"
}
```


## Getting Started

## Getting Help

## More guidance