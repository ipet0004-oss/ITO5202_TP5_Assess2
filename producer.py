# import statements
from pyspark.sql import SparkSession
from time import sleep
from json import dumps
from kafka3 import KafkaProducer
import random
import datetime as dt

def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
                                  value_serializer=lambda x: dumps(x).encode('ascii'),
                                  api_version=(0, 10))
    except Exception as ex:
        print('Exception while connecting Kafka.')
        print(str(ex))
    finally:
        return _producer

if __name__ == "__main__":

    topic = "events"

    #reads in steaming subset from Part A in batches (800 records per batch)
    batch_size = 800

    spark = SparkSession.builder.appName("Kafka Ride Producer").getOrCreate()

    #becuase the randomSplit uses seed=42, it will be reproducible for each instance. therefore the same code can be used in this file
    #and create stream_df with the exact same 30% data as with Assessment2 code
    df = spark.read.csv("ncr_ride_bookings.csv",header=True)
    _, stream_df = df.randomSplit([0.7, 0.3],seed=42)

    #check number of records matches Assessment2, which should be 44791
    print(f"Streaming subset contains "f"{stream_df.count()} records.")
    print("should contain 44791 records")

    records = [row.asDict()for row in stream_df.collect()]

    producer = connect_kafka_producer()

    if producer is None:
        print("Unable to connect to Kafka.")
        spark.stop()
        exit()

    batch_number = 1

    for start in range(0, len(records), batch_size):
        batch = records[start:start + batch_size]

       #add event_timestamp to each outgoing record using the time the batch is published
        event_timestamp = dt.datetime.now().isoformat()
        for record in batch:
            record["event_timestamp"] = event_timestamp

        #serialises each batch as a JSON array and publish it to kafta topic
        producer.send(topic,value=batch)

        # Ensure batch has been sent
        producer.flush()

        #logs the record count and timestamp of each batch to stdout
        print(f"Batch {batch_number}: " f"{len(batch)} records published at " f"{event_timestamp}")

        batch_number += 1

        #pauses for exactly 5 seconds between batches to simulate a controlled arrival rate
        sleep(5)

    producer.close()
    spark.stop()

    print("Finished publishing streaming data.")