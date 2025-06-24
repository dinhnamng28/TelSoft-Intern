from pyspark.sql import SparkSession
from config import configuration
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, DoubleType, IntegerType, LongType
from pyspark.sql.functions import col
from datetime import datetime

import sys
sys.path.append('/tmp/boto3')

import boto3
from urllib.parse import urlparse

#aws-java-sdk:1.11.469
def main():
    try:
        spark = SparkSession.builder.appName("SmartCityStreaming")\
            .config("spark.jars.packages",
                    "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0,"
                    "org.apache.hadoop:hadoop-aws:3.3.1,"
                    "com.amazonaws:aws-java-sdk-bundle:1.11.1000")\
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")\
            .config("spark.hadoop.fs.s3a.access.key", "your access key")\
            .config("spark.hadoop.fs.s3a.secret.key", "your secret key")\
            .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")\
            .config("spark.hadoop.security.authentication", "simple")\
            .getOrCreate()

    except Exception as e:
        print(f"Error creating Spark session: {e}")


    # Adjust the log level to minimize the console output on executors
    spark.sparkContext.setLogLevel("WARN")

    # Define schemas
    taxiSchema = StructType([
        StructField('id', StringType(),True),
        StructField('VendorID', IntegerType(),True),
        StructField('tpep_pickup_datetime', TimestampType(), True),
        StructField('tpep_dropoff_datetime', TimestampType(),True),
        StructField('passenger_count', IntegerType(),True),
        StructField('trip_distance', DoubleType(), True),
        StructField('pickup_longitude', DoubleType(), True),
        StructField('pickup_latitude', DoubleType(), True),
        StructField('RateCodeID', IntegerType(), True),
        StructField('store_and_fwd_flag', StringType(), True),
        StructField('dropoff_longitude', DoubleType(), True),
        StructField('dropoff_latitude', DoubleType(), True),
        StructField('payment_type', IntegerType(), True),
        StructField('fare_amount', DoubleType(), True),
        StructField('extra', DoubleType(), True),
        StructField('mta_tax', DoubleType(), True),
        StructField('tip_amount', DoubleType(), True),
        StructField('tolls_amount', DoubleType(), True),
        StructField('improvement_surcharge', DoubleType(), True),
        StructField('total_amount', DoubleType(), True)
    ])


    # Function to read data from Kafka
    def read_kafka_topic(topic, schema):
        return (spark.readStream
                .format('kafka')
                .option('kafka.bootstrap.servers', 'broker:29092')  # Update with your Kafka server
                .option('subscribe', topic)  # Corrected option name
                .option('startingOffsets', 'earliest')
                .option("failOnDataLoss", "true")
                .load()
                .selectExpr('CAST(value AS STRING)')
                .select(from_json(col('value'), schema).alias('data'))
                .select('data.*')
                .withWatermark('tpep_pickup_datetime', '2 minutes'))  # Ensure 'timestamp' is part of your schema



    def delete_s3_folder(s3_path):
        s3 = boto3.resource(
            's3',
            aws_access_key_id='',
            aws_secret_access_key=''
        )
        parsed = urlparse(s3_path, allow_fragments=False)
        bucket = parsed.netloc
        prefix = parsed.path.lstrip('/')

        bucket_obj = s3.Bucket(bucket)
        bucket_obj.objects.filter(Prefix=prefix).delete()

        print(f"✅ Đã xoá folder S3: s3://{bucket}/{prefix}")



    # Function to write data
    def streamWriter(DataFrame, checkpointFolder, output):
        return DataFrame.writeStream\
               .format('csv')\
               .option('checkpointLocation', checkpointFolder)\
               .option('path', output)\
               .option('header', 'true')\
               .outputMode('append')\
               .start()

    # Read data from Kafka topics
    taxiDF = read_kafka_topic('taxi_data', taxiSchema).alias('taxi')

    checkpoint_path = f"s3a://spark-streaming-data-lech/checkpoints/Taxi_data"
    output_path = f"s3a://spark-streaming-data-lech/data/Taxi_data"

    delete_s3_folder(output_path)

    query = streamWriter(taxiDF, checkpoint_path, output_path)

    #query = streamWriter(taxiDF, 's3a://spark-streaming-data-lech/checkpoints/Taxi_data', 's3a://spark-streaming-data-lech/data/Taxi_data')

    query.awaitTermination()

if __name__ == "__main__":
    main()
