from kafka import KafkaProducer
import json

def lambda_handler(event, context):
    print(event)
    request_body = json.loads(event['body'])
    name = request_body['name']
   
    # Upstash Kafka configuration
    upstash_bootstrap_servers = 'unified-cockatoo-8233-eu1-kafka.upstash.io:9092'
    upstash_username = 'dW5pZmllZC1jb2NrYXRvby04MjMzJD7PSBslPbwmPD-_Sxv2EUZZhI5dF6VkhoI'
    upstash_password = 'YzU3YjcwZTYtY2U2OS00YTQ5LWI5YjEtODRiNjY1MGM2MGY0'

    # Kafka Producer configuration
    producer_config = {
        'bootstrap_servers': upstash_bootstrap_servers,
        'sasl_mechanism': 'SCRAM-SHA-256',
        'security_protocol': 'SASL_SSL',
        'sasl_plain_username': upstash_username,
        'sasl_plain_password': upstash_password,
    }

    # Create a Kafka Producer
    producer = KafkaProducer(
        bootstrap_servers=producer_config['bootstrap_servers'],
        sasl_mechanism=producer_config['sasl_mechanism'],
        security_protocol=producer_config['security_protocol'],
        sasl_plain_username=producer_config['sasl_plain_username'],
        sasl_plain_password=producer_config['sasl_plain_password'],
    )

    try:
        data_to_store = []

        # Generate numbers from 10 to 100 and produce to Upstash Kafka
        # for i in range(10, 101):
        #     # Data to be stored in Upstash Kafka
        #     current_data = {'number': i}

            # Produce a message to the 'Athiva' Kafka topic
        producer.send('Athiva', json.dumps(name).encode('utf-8'))
            # data_to_store.append(current_data)
            # print(f"Data produced successfully for number {i}")

        return {
            'statusCode': 200,
            'body': json.dumps("kafka data produced successfully")
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    finally:
        producer.close()
