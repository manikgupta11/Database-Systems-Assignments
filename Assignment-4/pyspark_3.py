"""
Input format:
python3 pyspark_3.py <no_of_cpu> <output_file>

Set these environment variables in .bashrc file
export PYSPARK_PYTHON=/usr/bin/python3
export PYSPARK_DRIVER_PYTHON=/usr/bin/python3
"""
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark import SparkConf
import sys

if(len(sys.argv)!=3):
	print("Incorrect format provided \nInput format: python3 pyspark_3.py <no_of_cpu> <output_file>")
	sys.exit(0)

#Setting spark session and configuration
conf = SparkConf().setAppName("q3").setMaster("local")
sc = SparkContext(conf=conf)
spark = SparkSession.builder.appName("q3").master("local").getOrCreate()

#Read csv into dataframe
df = spark.read.csv('airports.csv', inferSchema=True, header=True)

#partition df according to no of cpu
no_of_cpu = int(sys.argv[1])
paritioned_df = df.repartition(no_of_cpu)
# print (paritioned_df.rdd.getNumPartitions())

#Apply transformation on df
result_rdd = paritioned_df.filter((paritioned_df['LATITUDE']>=10) & (paritioned_df['LATITUDE']<=90)  & (paritioned_df['LONGITUDE']<=-10)  & (paritioned_df['LONGITUDE']>=-90) ).collect()
result_df = spark.createDataFrame(result_rdd)

#Write outout to csv
result_df.repartition(1).write.csv(sys.argv[2])

