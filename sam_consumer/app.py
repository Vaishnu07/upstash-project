
import json
from confluent_kafka import Consumer, KafkaException
import boto3

def lambda_handler(event, context):
    s3_bucket_name = 'vaishnu-files'
    s3_prefix = 'Kafka consume/' 
    s3_path = s3_prefix + "data_consumed01"
        
    # Upstash Kafka configuration
    upstash_bootstrap_servers = 'unified-cockatoo-8233-eu1-kafka.upstash.io:9092'
    upstash_username = 'dW5pZmllZC1jb2NrYXRvby04MjMzJD7PSBslPbwmPD-_Sxv2EUZZhI5dF6VkhoI'
    upstash_password = 'YzU3YjcwZTYtY2U2OS00YTQ5LWI5YjEtODRiNjY1MGM2MGY0'

    # Kafka Consumer configuration
    consumer_config = {
        'bootstrap.servers': upstash_bootstrap_servers,
        'group.id': 'my-group',
        'sasl.mechanisms': 'SCRAM-SHA-256',
        'security.protocol': 'SASL_SSL',
        'sasl.username': upstash_username,
        'sasl.password': upstash_password,
        'auto.offset.reset': 'earliest'
    }
    
    # Create a Kafka Consumer
    consumer = Consumer(consumer_config)
    print(consumer)

    # Subscribe to the Kafka topic
    consumer.subscribe(['Athiva'])

    # Create an S3 client
    s3_client = boto3.client('s3')
    
    records = []
    for i in range(5):
        msg = consumer.consume(timeout=3.0)
        print(msg)
        if msg == []:
            print('hi')
        else:
            for i in msg:
                message = i.value().decode('utf-8')
                print(message)
                records.append(message)
    s3_client.put_object(Key=s3_path, Bucket=s3_bucket_name, Body=json.dumps(records).encode('UTF-8'))
    
    consumer.close()
 
