import json
from confluent_kafka import Producer, Consumer, KafkaException
from .kafka_admin import KafkaAdmin
from .logger import logger

# class kafka producer
class KafkaProducer:
    """
    Kafka Producer wrapper with logging and JSON serialization.
    """
    def __init__(self, bootstrap_servers: str, **producer_config):
        self.bootstrap_servers = bootstrap_servers
        self.admin = KafkaAdmin(bootstrap_servers=self.bootstrap_servers)
        config = {'bootstrap.servers': self.bootstrap_servers}
        config.update(producer_config)
        self.producer = Producer(config)

    def __str__(self):
        pass

    def send_message(self, topic: str, message: dict, on_delivery=None):
        try:
            # Assume topic is already created; don't create on every send
            serialized = json.dumps(message).encode('utf-8')
            self.producer.produce(topic, serialized, callback=on_delivery or self._delivery_report)
            logger.info(f"Message produced to topic '{topic}'", func_name=self.send_message.__name__)
        except Exception as e:
            logger.error(f"Producer error: {e}", func_name=self.send_message.__name__)
            raise KafkaException(e)

    def _delivery_report(self, err, msg):
        if err is not None:
            logger.error(f"Delivery failed for message: {err}", func_name=self._delivery_report.__name__)
        else:
            logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}", func_name=self._delivery_report.__name__)

    def flush(self):
        self.producer.flush()

    def close(self):
        self.flush()
        logger.info("Producer closed", func_name=self.close.__name__)

# class kafka consumer
class KafkaConsumer:
    """
    Kafka Consumer wrapper with logging and topic subscription.
    """
    def __init__(self, bootstrap_servers: str, group_id: str = 'book-group', topics=None, **consumer_config):
        self.bootstrap_servers = bootstrap_servers
        config = {
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
        }
        config.update(consumer_config)
        self.consumer = Consumer(config)
        self.topics = topics or []
        if self.topics:
            self.consumer.subscribe(self.topics)
            logger.info(f"Subscribed to topics: {self.topics}", func_name=self.__init__.__name__)

    def __str__(self):
        pass

    def receive_message(self, timeout: float = 1.0):
        try:
            msg = self.consumer.poll(timeout=timeout)
            if msg is None:
                return None
            if msg.error():
                logger.error(f"Consumer error: {msg.error()}", func_name=self.receive_message.__name__)
                raise KafkaException(msg.error())
            logger.info(f"Received message from {msg.topic()} [{msg.partition()}] at offset {msg.offset()}", func_name=self.receive_message.__name__)
            
            return msg
        except Exception as e:
            logger.error(f"Consumer poll error: {e}", func_name=self.receive_message.__name__)
            raise KafkaException(e)

    def receive_batch(self, batch_size: int = 10, timeout: float = 1.0):
        messages = []
        for _ in range(batch_size):
            msg = self.receive_message(timeout)
            if msg:
                messages.append(msg)
        return messages

    def close(self):
        self.consumer.close()
        logger.info("Consumer closed", func_name=self.close.__name__)

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
