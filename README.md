# payment System Craft Demo
This Payment System demo repo provides brief workflow operates on AWS along with deployed Risk Engine application as well as details on Wiki document.

## Jump to:
- [Payment System REST APIs](#1-REST-API-guidance)
- [Payload attributes](#2-Payload-attributes)
- [Getting Started](#3-Getting-Started)
- [Getting Help](#4-Getting-Help)
- [More guidance](#5-Further-Reading)

# 1. REST API guidance
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
Status: 201 Created
{
  "StatusCode": 201,
  "Status": "Success",
  "PaymentId": "5565f337-c901-458c-bab8-20fcf12ba573"
}
```

The response contains the `Result`, `PaymentId` and `status` indicating the payment is successfully completed. An optional addtiributes can also be returned in the near future if needed.



# 2. Payload attributes

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

# 3. Getting Started
This guide will walk you through setting up and running the Risk Engine python application in a Docker container.

## Prerequisites
- Docker installed on your machine. See which platform you need in the following official Docker installation [document](https://docs.docker.com/engine/install/)
- Clone this repository

## Build Docker Image
Clone the Risk Engine repository and navigate to the project directory:
```
git clone https://github.com/HaeyoonJo/intuit_MLOps_paymentSystem_craft_demo.git
cd intuit_MLOps_paymentSystem_craft_demo
```

Build the Docker image from the Dockerfile:  

We won't version the tag(s), however, the best practice is versioning your Docker Image(s) using `tag`. See how to use [Docker Image tag](https://docs.docker.com/engine/reference/commandline/image_tag/).  

This builds the image and tags it as `risk-engine`
```
docker build -t risk-engine .
```

## Create a Docker Network
One of best practices to run containers in a custom network so they can communicate or isolate from other containers. Create a network:

```
docker network create risk-engine-net
```

## Run the Container
Run the `risk-engine` image in a container attached to the network.  

This runs the container detached, names it `risk-engine`, attaches it to `risk-engine-net`, publishes port 5000, and uses the `risk-engine` image.

```
docker run --name risk-engine --network risk-engine-net --rm -p 5000:5000 risk-engine
```

The app should now be running on http://localhost:5000!

## Test Risk Engine
Once the container is up and running, you can send request using terminal or postman or any other tools that handy for you.

Example request provided below
```
$ curl -X POST -H "Content-Type: application/json" -d '{"amount": 70.5, "currency": "USD", "userId": "e8af92bd-1910-421e-8de0-cb3dcf9bf44d", "payeeId": "4c3e304e-ce79-4f53-bb26-4e198e6c780a", "paymentMethodId": "8e28af1b-a3a0-43a9-96cc-57d66dd68294"}' http://localhost:5000/payments
{
  "StatusCode": 201,
  "Status": "Success",
  "PaymentId": "3be0f9fc-3cdf-44d3-8524-b882f4ff0d80"
}
```

## Shut Down and Clean Up
Container will be removed automatically as we used `--rm` option in `docker run` command.

To remove the network and Image:
```
docker network rm risk-engine-net
docker rmi risk-engine
```

# 4. Getting Help

If you need any help with setting up or running Risk Engine, have questions, or run into any issues, there are a couple ways to get assistance:

### GitHub Issues  
We welcome bug reports, feature requests, and questions in the GitHub issue tracker for Risk Engine. Open an issue describing your problem or question here:

https://github.com/HaeyoonJo/intuit_MLOps_paymentSystem_craft_demo/issues/

Make sure to include details like your operating system, Docker version, steps to reproduce issues, and any error messages you are getting.

I monitor issues frequently and will provide support.

### Email  
For time-sensitive inquiries or privacy concerns, you can email me directly at haeyoon.devops@gmail.com.

Please only use the email for urgent or private matters - for other requests, opening a GitHub issue is preferred so solutions can benefit others.

I will try to respond to emails within 3 business days.


# 5. Further Reading

This Getting Started guide covers the basics of running Risk Engine in Docker for development and testing purposes.

For guidance on additional configurations and production deployments, see our in-depth technical documentation:

### Payment System Wiki
The Payment System Wiki contains extensive guides and references for:
- Payment System architecture
- Risk Engine REST API design
- Workflow and deployment to production
- Code overviews
- Release notes and changes

Wiki: https://github.com/HaeyoonJo/intuit_MLOps_paymentSystem_craft_demo/wiki