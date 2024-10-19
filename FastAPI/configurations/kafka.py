from confluent_kafka import Producer, Consumer, KafkaException
from .kafka_admin import KafkaAdmin

# class kafka producer
class KafkaProducer:
    """
    A class representing a Kafka producer.
    Attributes:
    bootstrap_servers (str): The bootstrap servers for the Kafka producer.
    producer (Producer): The Kafka producer object.
    """
    def __init__(self, bootstrap_servers):

        self.bootstrap_servers = bootstrap_servers
        self.admin = KafkaAdmin(bootstrap_servers=self.bootstrap_servers)

        self.producer = Producer(config={
            'bootstrap_servers': self.bootstrap_servers,
            'auto.offset.reset': 'earliest'
        })

    def __str__(self):
        pass

    def send_message(self, topic, message):

        try:
            self.admin.create_topic(topic)
            self.producer.produce(topic, message.encode('utf-8'))
            self.commit()
        except Exception as e:
            raise KafkaException(e)

    def commit(self):
        self.producer.flush()

    def close(self):
        self.producer.close()

# class kafka consumer
class KafkaConsumer:
    """
    A class representing a Kafka consumer.
    Attributes:
    bootstrap_servers (str): The bootstrap servers for the Kafka consumer.
    consumer (Consumer): The Kafka consumer object.
    """
    def __init__(self, bootstrap_servers):

        self.bootstrap_servers = bootstrap_servers

        self.consumer = Consumer(config={
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': 'book-group',
            'auto.offset.reset': 'earliest'
        })

    def __str__(self):
        pass

    def receive_message(self):

        try:
            message = self.consumer.poll(timeout=1.0)
            if message is None:
                return None
            if message.error():
                raise KafkaException(message.error())
            else:
                return message
        except Exception as e:
            raise KafkaException(e)

    def close(self):
        self.consumer.close()

# if __name__ == '__main__':
#     p = KafkaProducer(KAFKA_BROKER)
#     message = input("Enter message: ")
#
#     p.send_message(KAFKA_TOPIC, message = message)
#     p.commit()
#     p.close()


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
