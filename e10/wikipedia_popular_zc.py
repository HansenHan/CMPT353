import sys
import re
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('reddit averages').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+


wiki_schema = types.StructType([
    types.StructField('language', types.StringType()),
    types.StructField('title', types.StringType()),
    types.StructField('request', types.IntegerType()),
    types.StructField('bytes', types.IntegerType())
])

def find_path(path):
    return re.search("\d{8}-\d{2}",path)[0]

def main(in_directory, out_directory):
    data = spark.read.csv(in_directory, schema=wiki_schema, sep = ' ' ).withColumn('filename', functions.input_file_name())
    data = data.filter(data['language']=='en')
    data = data.filter(data['title']!='Main_Page')
    data = data.drop(data['title'].startswith('Special:'))

    path_to_hour = functions.udf(find_path, returnType=types.StringType())
    data = data.withColumn('date', path_to_hour(data['filename'])).cache()
    # data = data.cache()
    group_data = data.groupby('date').max('request')
    data = data.join(group_data,'date')
    # data = data.cache()
    data = data[data['request']==data['max(request)']].select('date','title','request')
    data = data.sort(data['date'],data['title'])
    data.show(100)
    # data = data.cache()
    data = data.write.csv(out_directory, mode='overwrite')

if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)

