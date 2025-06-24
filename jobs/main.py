# import os
# from confluent_kafka import SerializingProducer
# import simplejson as json
# import uuid
# import pandas as pd

# CSV_PATH = 'jobs/yellow_tripdata_2015-01.csv'

# #environments variable for config
# KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
# TAXI_NYC_TOPIC = os.getenv('TAXI_NYC_TOPIC', 'taxi_data')


# def taxi_nyc_data():
#     df = pd.read_csv(CSV_PATH)

#     # Chuyển mỗi dòng thành dict, có thể thêm UUID nếu muốn
#     for _, row in df.iterrows():
#         data = row.to_dict()
#         data['id'] = uuid.uuid4()
#         yield data

# def json_serializer(obj):
#     if isinstance(obj, uuid.UUID):
#         return str(obj)
#     raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

# def delivery_report(err, msg):
#     if err is not None:
#         print(f'Message delivery failed: {err}')
#     else:
#         print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

# def producer_data_to_kafka(producer, topic, data):
#     producer.produce(
#         topic,
#         key=str(data['id']),
#         value=json.dumps(data, default=json_serializer).encode('utf-8'),
#         on_delivery=delivery_report
#     )

# def simulate_journey(producer, device_id=None):
#     for taxi_data in taxi_nyc_data():
#         producer_data_to_kafka(producer, TAXI_NYC_TOPIC, taxi_data)
#         producer.flush()

# if __name__ == "__main__":
#     producer_config = {
#         'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
#         'error_cb': lambda err: print(f'Kafka error: {err}') 
#         }
    
#     producer = SerializingProducer(producer_config)
    
#     try:
#         simulate_journey(producer, 'Taxi-DinhNamNguyen')
#     except KeyboardInterrupt:
#         print('Simulation ended by the user')
#     except Exception as e:
#         print(f'Unexpected Error occured: {e}')

import os
import uuid
import pandas as pd
from confluent_kafka import Producer
import simplejson as json

CSV_PATH = 'jobs/yellow_tripdata_2015-01.csv'

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
TAXI_NYC_TOPIC = os.getenv('TAXI_NYC_TOPIC', 'taxi_data')


def taxi_nyc_data():
    chunksize = 1000  # đọc theo từng chunk để tiết kiệm RAM
    for chunk in pd.read_csv(CSV_PATH, chunksize=chunksize):
        for _, row in chunk.iterrows():
            data = row.to_dict()
            data['id'] = uuid.uuid4()
            yield data


def json_serializer(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')


def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')


def producer_data_to_kafka(producer, topic, data):
    producer.produce(
        topic=topic,
        key=str(data['id']),
        value=json.dumps(data, default=json_serializer).encode('utf-8'),
        callback=delivery_report
    )


def simulate_journey(producer):
    batch_size = 1000
    count = 0
    for taxi_data in taxi_nyc_data():
        producer_data_to_kafka(producer, TAXI_NYC_TOPIC, taxi_data)
        count += 1
        if count % batch_size == 0:
            producer.flush()
            print(f'Đã gửi {count} dòng')
    producer.flush()
    print(f'Hoàn tất gửi {count} dòng')


if __name__ == "__main__":
    producer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'error_cb': lambda err: print(f'Kafka error: {err}')
    }

    producer = Producer(producer_config)

    try:
        simulate_journey(producer)
    except KeyboardInterrupt:
        print('Simulation ended by the user')
    except Exception as e:
        print(f'Unexpected Error occurred: {e}')
