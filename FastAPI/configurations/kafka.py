from confluent_kafka import Producer, Consumer, KafkaError, KafkaException
import json
import os
from dotenv import load_dotenv
load_dotenv()
KAFKA_BROKER = os.getenv("KAFKA_BROKER", str)
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", str)

def get_kafka_producer():
    producer = Producer({
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': 'book-group',
        'auto.offset.reset': 'earliest'
    })

    producer.subscribe([KAFKA_TOPIC])
    return producer

def get_kafka_consumer():
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': 'book-group',
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe([KAFKA_TOPIC])
    return consumer

def send_kafka_message(producer, message):
    producer.produce(KAFKA_TOPIC, message.encode('utf-8'))
    producer.flush()

    return True

def receive_kafka_message(consumer):

    message = consumer.poll(timeout=1.0)
    if message is None:
        return None
    if message.error():
        raise KafkaException(message.error())
    else:
        return message.value().decode('utf-8')

    return message.value().decode('utf-8')

def close_kafka_producer(producer):
    producer.flush()
    producer.close()

def close_kafka_consumer(consumer):
    consumer.close()

    return True

def get_kafka_broker():
    return KAFKA_BROKER


# def get_kafka_producer():
#     producer = Producer({
#         'bootstrap.servers': KAFKA_BROKER,
#         'group.id': 'group1',
#         'auto.offset.reset': 'earliest'
#     })
#
#     producer.subscribe([KAFKA_TOPIC])
#     return producer
#
# def get_kafka_consumer():
#     consumer = Consumer({
#         'bootstrap.servers': KAFKA_BROKER,
#         'group.id': 'group1',
#         'auto.offset.reset': 'earliest'
#     })
#
#     consumer.subscribe([KAFKA_TOPIC])
#     return consumer
