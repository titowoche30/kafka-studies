from fake_web_events import Simulation
from kafka import KafkaProducer
import json
import random
import time
import argparse


def get_events(user_pool_size, sessions_per_day, duration_seconds):
    simulation = Simulation(user_pool_size=user_pool_size, sessions_per_day=sessions_per_day)
    events = simulation.run(duration_seconds=duration_seconds)

    return events


def get_producer(key_serializer, value_serializer, bootstrap_servers=['localhost:9092'], client_id='cwoche-python', acks='all'):
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                             client_id=client_id,
                             key_serializer=key_serializer,
                             value_serializer = value_serializer,
                             acks=acks,
                             linger_ms=0,
                             batch_size=16384)

    '''
     linger.ms refers to the time to wait before sending messages out to Kafka.
     It defaults to 0, which the system interprets as send messages as soon as they are ready to be sent.

     batch.size refers to the maximum amount of data to be collected before sending the batch.

     Kafka producers will send out the next batch of messages whenever linger.ms or batch.size is met first. 
    '''

    return producer


def send_events(producer, events, topic='cwoche-topic', n_partitions=2):
    aux = 0
    print('\nSending events to Kafka...')
    for event in events:
        rand = random.randint(1, n_partitions)
        producer.send(topic=topic,key=rand,value=event)
        aux += 1

    print(f'\n{aux} events were sent')

    producer.flush()
    print(f'\n{producer.metrics()}')
    producer.close()


if __name__ == '__main__':
    '''
    $ python producer.py -d 10
    
    usage: producer.py [-h] [-p POOL_SIZE] [-s SESSIONS_DAY] [-d DURATION_SECONDS]

    Python Kafka Producer
    
    optional arguments:
      -h, --help            show this help message and exit
      -p POOL_SIZE, --pool_size POOL_SIZE
                            The user_pool_size used to simulate the events
      -s SESSIONS_DAY, --sessions_day SESSIONS_DAY
                            The sessions_per_day used to simulate the events
      -d DURATION_SECONDS, --duration_seconds DURATION_SECONDS
                            The duration_seconds of the simulation
    '''

    parser = argparse.ArgumentParser(description='Python Kafka Producer')
    parser.add_argument("-p", "--pool_size",
                        help="The user_pool_size used to simulate the events", default=100, type=int)
    parser.add_argument("-s", "--sessions_day",
                        help="The sessions_per_day used to simulate the events", default=10, type=int)
    parser.add_argument("-d", "--duration_seconds",
                        help="The duration_seconds of the simulation", default=15, type=int)

    args = parser.parse_args()

    events = get_events(user_pool_size=args.pool_size,
                        sessions_per_day=args.sessions_day,
                        duration_seconds=args.duration_seconds)

    producer = get_producer(key_serializer=lambda k: json.dumps(k).encode('utf-8'),
                            value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    t0 = time.time()
    send_events(producer, events)
    print(f'\nit took {time.time()- t0} seconds to send')

