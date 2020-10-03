"""
Input format:
python3 pyspark_1.py <no_of_cpu> <output_file>

Set these environment variables in .bashrc file
export PYSPARK_PYTHON=/usr/bin/python3
export PYSPARK_DRIVER_PYTHON=/usr/bin/python3
"""
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark import SparkConf
import sys

if(len(sys.argv)!=3):
	print("Incorrect format provided \nInput format: python3 pyspark_1.py <no_of_cpu> <output_file>")
	sys.exit(0)

#Setting spark session and configuration
conf = SparkConf().setAppName("q1").setMaster("local")
sc = SparkContext(conf=conf)
spark = SparkSession.builder.appName("q1").master("local").getOrCreate()

#Read csv into dataframe
df = spark.read.csv('airports.csv', inferSchema=True, header=True)

#partition df according to no of cpu
no_of_cpu = int(sys.argv[1])
paritioned_df = df.repartition(no_of_cpu)
# print(paritioned_df.rdd.getNumPartitions())

#Group countries by airports count
df_groupby=paritioned_df.groupby("COUNTRY").count()

#Write result in output file
df_groupby.repartition(1).write.csv(sys.argv[2])


