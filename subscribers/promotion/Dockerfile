FROM python:3.8-slim-buster

WORKDIR /app

# Copy dependency file
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip3 install -r requirements.txt

# Add source code into container image in path /app
COPY . /app

# Start the service
CMD ["python3", "promotion.py"]