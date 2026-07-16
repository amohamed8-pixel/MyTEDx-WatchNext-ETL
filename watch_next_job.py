import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, collect_list
from awsglue.dynamicframe import DynamicFrame

# 1. Inizializzazione 
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# 2. EXTRACT: Lettura da S3
s3_input_path = "s3://mytedx-data-bucket-1100748/watch_next_dataset.csv"

df = spark.read.option("header", "true").csv(s3_input_path)

# 3. TRANSFORM: Pulizia e raggruppamento
df_clean = df.dropna(subset=["video_id", "watch_next_video_id"])
df_transformed = df_clean.groupBy("video_id") \
    .agg(collect_list("watch_next_video_id").alias("recommended_talks"))

dynamic_frame_write = DynamicFrame.fromDF(df_transformed, glueContext, "dynamic_frame_write")

# 4. LOAD: Scrittura su DynamoDB
glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame_write,
    connection_type="dynamodb",
    connection_options={
        "dynamodb.output.tableName": "MyTEDx_WatchNext_Table",
        "dynamodb.throughput.write.percent": "1.0"
    }
)

job.commit()
