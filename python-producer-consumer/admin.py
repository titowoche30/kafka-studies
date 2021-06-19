from kafka.admin import KafkaAdminClient, NewTopic

admin_client = KafkaAdminClient(bootstrap_servers=['localhost:9092'],
                                client_id='cwoche-python'
                                )


def list_consumer_groups():
    admin_client.list_consumer_groups()


def create_topic(name, num_partitions, replication_factor):
    my_topic = NewTopic('cwoche-topic',
                        num_partitions=num_partitions,
                        replication_factor=replication_factor)

    admin_client.create_topics([my_topic])


def delete_topics(topics):
    admin_client.delete_topics(topics)


if __name__ == '__main__':
    topic_name = 'cwoche-topic'
    # create_topic(topic_name, 2, 2)
    # delete_topics([topic_name])
    print(list_consumer_groups())
    admin_client.close()


