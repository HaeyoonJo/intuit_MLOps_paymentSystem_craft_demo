# payment System Craft Demo
This Payment System demo repo provides brief workflow operates on AWS along with deployed Risk Engine application as well as details on Wiki document.

> Unfortunately, I couldn't prepare Question "6. simple Spark code". This will be commit within 9th Jan, Tue under /Spark directory. Also follow up the status in https://github.com/HaeyoonJo/intuit_MLOps_paymentSystem_craft_demo/issues/18

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

This guide will walk you through setting up and running the Payment System demo including Payment System, Rabbit MQ, Risk Engine using Docker Compose, which simplifies the process of managing multi-container Docker applications.

## Prerequisites

- Docker and Docker Compose installed on your machine. If you do not have them installed, follow the official Docker installation guide [here](https://docs.docker.com/get-docker/) and the Docker Compose installation guide [here](https://docs.docker.com/compose/install/).

## Clone the Repository

Clone the repository to your local machine using the following command:
```
git clone https://github.com/HaeyoonJo/intuit_MLOps_paymentSystem_craft_demo.git
cd intuit_MLOps_paymentSystem_craft_demo
```

## Configure the Environment

Before running the application, you may need to configure environment variables used by the Docker containers. In this demo, `rabbitmq` service requires but I put in the compose file for demo. If required, create a `.env` file in the root directory and specify the necessary variables.

Example `.env` file:
```
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=password
```
Example `docker-compose.yml` file:
```
env_file:
  - .env
```

## Run Docker Compose

Navigate to the directory containing your `docker-compose.yml` file and run the following command to start all services defined in the Docker Compose configuration:
```bash
docker compose up --build
```
If you wish to run it in background (detached mode), use `-d` flag.

## Verify the Application

After starting the services, you can verify that Payment System is up and running by checking the logs of each container. 

Replace `<container-id>` with the actual ID of your Risk Engine container. You can find the container ID by running `docker ps` and looking for the container running the Risk Engine.

In the logs, look for a message similar to the following:
```
$ docker logs 12538163f43e
Waiting for messages...
Received message: b'{"payment_data": {...}, "payment_id": "9e0f1934-3c9c-4b45-87e6-52a5acc89301"}'
Payment 9e0f1934-3c9c-4b45-87e6-52a5acc89301 approved. Random num: 0.45945097007442726
```

This log entry indicates that the payment with ID `9e0f1934-3c9c-4b45-87e6-52a5acc89301` has been processed and approved by the Risk Engine. If the payment were declined, the log would instead indicate that the payment was declined.

Please note that the `Random num` is part of the risk analysis simulation, where a random number determines the approval of the payment. In a real-world scenario, this would be replaced with actual risk assessment logic.


## Checking Payment Status

The Risk Engine logs each payment it processes, including the payment ID and the result of the risk analysis. To check the status of a specific payment, you can look at the Risk Engine's logs.


## Interact with the Risk Engine

With the Risk Engine running, you can now interact with it using the defined APIs or by sending messages to the configured RabbitMQ queues.


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

When you are done, you can stop and remove the containers, networks, and volumes created by Docker Compose using the following command:
```bash
docker-compose down
```

Optionally, to remove all images used by any service in the `docker-compose.yml` file, add the `--rmi all` flag:
```bash
docker-compose down --rmi all
```

This will help you keep your development environment clean and ensure that fresh containers are created the next time you run `docker-compose up`.

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