import os
import sys
import json
import uuid
import boto3
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

aws_region = os.getenv("AWS_DEFAULT_REGION", default='eu-west-1')
sqs_client = boto3.client('sqs', region_name=aws_region)

def get_messages(uri):
    messages = sqs_client.receive_message(QueueUrl=uri, 
                                          WaitTimeSeconds=5)
    
    return messages.get('Messages', [])

def delete_message(queue_uri, receipt):
    try:
        return sqs_client.delete_message(QueueUrl=queue_uri, 
                                         ReceiptHandle=receipt)
    except boto3.ClientError:
        logging.exception(f'Error deleting the message from {queue_uri}')
    
def process_message():
    queue_uri = os.environ.get('COPILOT_QUEUE_URI')
    
    # Process messages
    for message in get_messages(queue_uri):
        logging.info('Processing message Received from SNS')
        
        # Print out the name  with a slanted effect
        coupon_code = str(uuid.uuid4())[:8]
        message_body = json.loads(message['Body'])['Message']
        customer_name = json.loads(message_body)['customer']
        
        logging.info(f'\n Hey {customer_name}!\n Thanks for your order, you ' +\
            "have qualified for a 20% off on your next purchase.\n" +\
            f"Use coupon --- {coupon_code} --- on you next purchase.")
        
        # Message is processed, delete it from the queue
        delete_message(queue_uri, message.get('ReceiptHandle'))
        

if __name__ == '__main__':
    while True:
        process_message()