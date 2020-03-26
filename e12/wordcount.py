import sys
import string, re
import numpy as np
from pyspark.sql import SparkSession, functions

spark = SparkSession.builder.appName('wordcount').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5)
assert spark.version >= '2.3'

def main(in_directory, out_directory):
    data = spark.read.text(in_directory)
    # data.show()

    wordbreak = r'[%s\s]+' % (re.escape(string.punctuation),)
    data = data.withColumn('word', functions.explode(functions.split('value',wordbreak)))
    # data.show()

    data = data.withColumn('word', functions.lower(data['word']))
    data = data.filter(data['word'] != '')
    data = data.select('word')

    data.cache()
    data = data.groupBy('word').agg(functions.count(data['word']))
    # data.show()

    data = data.sort(functions.desc('count(word)'), functions.asc('word'))
    data = data.withColumnRenamed('count(word)', 'count')
    # data.show()

    data.write.csv(out_directory, mode = 'overwrite')

if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)

