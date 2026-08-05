import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, IntegerType

# Inizializzazione contesto Glue & Spark
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# 1. READ RAW DATA FROM S3
s3_path = "s3://my-tedx-bucket-landing/raw_tedx.csv"
raw_df = spark.read.option("header", "true").option("inferSchema", "true").csv(s3_path)

# 2. DATA CLEANING
clean_df = raw_df.filter(F.col("video_id").isNotNull())

# 3. SELF-JOIN PER CALCOLO "WATCH NEXT" (Raccomandazioni)
watch_next_df = clean_df.alias("a").join(
    clean_df.alias("b"),
    (F.col("a.main_tag") == F.col("b.main_tag")) & (F.col("a.video_id") != F.col("b.video_id")),
    "inner"
).groupBy("a.video_id").agg(
    F.collect_list(F.col("b.video_id")).alias("recommended_talks"),
    F.lit("Correlazione basata sui temi del talk").alias("reason")
)

# 4. EMBEDDING DEL QUIZ ENGINE (Active Learning)
transformed_df = clean_df.join(watch_next_df, "video_id", "left").withColumn(
    "quiz",
    F.array(
        F.struct(
            F.lit("Qual è il tema principale affrontato in questo talk?").alias("question"),
            F.array(
                F.lit("Innovazione e Tecnologia"),
                F.lit("Sviluppo Personale e Società"),
                F.lit("Scienza e Ricerca Applicata")
            ).alias("options"),
            F.lit(0).alias("correct_idx")
        )
    )
)

# 5. WRITE TO DYNAMODB SINK
glueContext.write_dynamic_frame.from_options(
    frame=DynamicFrame.fromDF(transformed_df, glueContext, "transformed_df"),
    connection_type="dynamodb",
    connection_options={
        "tableName": "tedx_data",
        "dynamodb.output.retry": "20"
    }
)

job.commit()
