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
COPY *.py .

CMD ["python", "-u", "app.py"]
