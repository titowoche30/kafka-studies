from fake_web_events import Simulation
from kafka import KafkaProducer
import json
import random


def get_events(user_pool_size=100, sessions_per_day=10, duration_seconds=15):
    simulation = Simulation(user_pool_size=user_pool_size, sessions_per_day=sessions_per_day)
    events = simulation.run(duration_seconds=duration_seconds)

    return events


def get_producer(key_serializer, value_serializer, bootstrap_servers=['localhost:9092'], client_id='cwoche-python', acks='all'):
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                             client_id=client_id,
                             key_serializer=key_serializer,
                             value_serializer = value_serializer,
                             acks=acks)

    return producer


def send_events(producer, events, topic='cwoche-topic', n_partitions=2):
    for event in events:
        rand = random.randint(1, n_partitions)
        producer.send(topic=topic,
                      key=rand,
                      value=event)

    producer.flush()
    print(producer.metrics())
    producer.close()


if __name__ == '__main__':
    events = get_events()
    producer = get_producer(key_serializer=lambda k: json.dumps(k).encode('utf-8'),
                            value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    send_events(producer, events)

