from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException

class KafkaAdmin:
    def __init__(self, bootstrap_servers):
        self.admin_client = AdminClient({"bootstrap.servers": bootstrap_servers})

    def get_topics(self, topic=None):
        return self.admin_client.list_topics(topic)

    def get_one_topic(self, topic):
        return self.get_topics([topic])

    def is_topic_exists(self, topic):
        return topic in self.get_topics().keys()

    def delete_topic(self, topic):
        if not self.is_topic_exists(topic):
            raise KafkaException(f"Topic {topic} does not exist")
        self.admin_client.delete_topics([topic])

    def create_topic(self, topic):
        if not self.is_topic_exists(topic):
            self.admin_client.create_topics([NewTopic(topic, num_partitions=1, replication_factor=1)])


    def close(self):
        self.admin_client.close()