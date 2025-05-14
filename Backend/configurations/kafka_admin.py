from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException
from .logger import logger

class KafkaAdmin:
    """
    Kafka Admin wrapper with logging and improved topic management.
    """
    def __init__(self, bootstrap_servers: str):
        self.admin_client = AdminClient({"bootstrap.servers": bootstrap_servers})

    def get_topics(self, topic: str = None):
        """
        Get all topics or a single topic by name.
        """
        try:
            metadata = self.admin_client.list_topics(topic)
            
            logger.info(f"Fetched topics: {list(metadata.topics.keys())}", func_name=self.get_topics.__name__)
            
            return metadata

        except Exception as e:
            logger.error(f"Error fetching topics: {e}", func_name=self.get_topics.__name__)
            raise KafkaException(e)

    def get_one_topic(self, topic):
        """
        Get a single topic by name.
        """
        try:
            return self.get_topics([topic])
        except Exception as e:
            logger.error(f"Error fetching topic: {e}", func_name=self.get_one_topic.__name__)
            raise KafkaException(e)

    def is_topic_exists(self, topic: str) -> bool:
        """
        Check if a topic exists.
        """
        try:
            return topic in self.get_topics().topics.keys()
        except Exception as e:
            logger.error(f"Error checking topic existence: {e}", func_name=self.is_topic_exists.__name__)
            return False

    def delete_topic(self, topic: str):
        if not self.is_topic_exists(topic):
            logger.warning(f"Topic {topic} does not exist", func_name=self.delete_topic.__name__)
            raise KafkaException(f"Topic {topic} does not exist")
        try:
            self.admin_client.delete_topics([topic])
            logger.info(f"Deleted topic: {topic}", func_name=self.delete_topic.__name__)
        except Exception as e:
            logger.error(f"Error deleting topic: {e}", func_name=self.delete_topic.__name__)
            raise KafkaException(e)

    def create_topic(self, topic: str, num_partitions: int = 1, replication_factor: int = 1):
        if not self.is_topic_exists(topic):
            try:
                self.admin_client.create_topics([NewTopic(topic, num_partitions=num_partitions, replication_factor=replication_factor)])
                logger.info(f"Created topic: {topic}", func_name=self.create_topic.__name__)
            except Exception as e:
                logger.error(f"Error creating topic: {e}", func_name=self.create_topic.__name__)
                raise KafkaException(e)
        else:
            logger.info(f"Topic {topic} already exists", func_name=self.create_topic.__name__)

    def close(self):
        self.admin_client.close()
        logger.info("Admin client closed", func_name=self.close.__name__)