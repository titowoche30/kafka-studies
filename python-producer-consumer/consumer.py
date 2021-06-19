import json
from kafka import KafkaConsumer, TopicPartition


def get_consumer(key_deserializer, value_deserializer,
                 bootstrap_servers = ['localhost:9092'],
                 client_id = 'cwoche-python',
                 group_id='cwoche-topic-group',
                 auto_offset_reset='earliest',
                 consumer_timeout_ms=6000):

    consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers,
                             client_id=client_id,
                             group_id=group_id,
                             key_deserializer=key_deserializer,
                             value_deserializer=value_deserializer,
                             # value_deserializer=lambda v: json.loads(v),
                             auto_offset_reset=auto_offset_reset,
                             consumer_timeout_ms=consumer_timeout_ms
                             )

    return consumer


if __name__ == '__main__':
    consumer = get_consumer(key_deserializer=lambda k: json.loads(k), value_deserializer=lambda v: json.loads(v))
    print(consumer.topics())

    # Choose either subscribe or assign

    consumer.subscribe(['cwoche-topic'])

    # partition = TopicPartition('cwoche-topic', 0)
    # consumer.assign([partition])

    for event in consumer:
        print(f'\n key = {event.key}')
        print(f'partition = {event.partition}')
        print(f'value = {event.value}')

    print(f'\n {consumer.metrics()}')
    consumer.close()
