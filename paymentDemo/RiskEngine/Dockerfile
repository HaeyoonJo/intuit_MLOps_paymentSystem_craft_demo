FROM python:3.8-slim-buster

# deprecated MAINTAINER
# MAINTAINER="Haeyoon Jo" 
LABEL maintainer="haeyoon.devops@gmail.com"

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY app.py \
        rabbitmq_utils.py \
        risk_analysis.py \
        risk_engine_handler.py \
        .

CMD ["python", "-u", "app.py"]