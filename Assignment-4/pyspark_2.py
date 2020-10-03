"""
Input format:
python3 pyspark_2.py <no_of_cpu> <output_file>

Set these environment variables in .bashrc file
export PYSPARK_PYTHON=/usr/bin/python3
export PYSPARK_DRIVER_PYTHON=/usr/bin/python3
"""
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark import SparkConf
import sys

if(len(sys.argv)!=3):
	print("Incorrect format provided \nInput format: python3 pyspark_2.py <no_of_cpu> <output_file>")
	sys.exit(0)

#Setting spark session and configuration
conf = SparkConf().setAppName("q2").setMaster("local")
sc = SparkContext(conf=conf)
spark = SparkSession.builder.appName("q2").master("local").getOrCreate()

#Read csv into dataframe
df = spark.read.csv('airports.csv', inferSchema=True, header=True)

#partition df according to no of cpu
no_of_cpu = int(sys.argv[1])
paritioned_df = df.repartition(no_of_cpu)
# print(paritioned_df.rdd.getNumPartitions())

#Group countries by airports count
df_groupby=paritioned_df.groupby("COUNTRY").count()

#Finding country with max count
max_val = df_groupby.agg({"count": "max"}).collect()[0][0]
result_country=df_groupby.filter(df_groupby['count']==max_val).collect()[0][0]

#Write result in output file
f = open(sys.argv[2], "w")
f.write(result_country)
f.close()


