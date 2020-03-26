import sys
import re
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('wikipedia popular').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

my_schema = types.StructType([
    types.StructField('language', types.StringType()),
    types.StructField('title', types.StringType()),
    types.StructField('time', types.IntegerType()),
    types.StructField('byte', types.IntegerType()),
])


def get_hour(date):
    date = date.split('/')[-1]
    return date[11:22]

    # date = date.split('-')[-2]+'-'+date.split('-')[-1]
    # return date[0:11]

    # return date[-18:-7] ## False!!

    # return re.search("\d{8}-\d{2}",date)[0]


def main(in_directory, out_directory):
    data = spark.read.csv(in_directory, schema = my_schema, sep = ' ' ).withColumn('filename', functions.input_file_name())

    path_to_hour = functions.udf(get_hour, returnType = types.StringType())
    data = data.withColumn('hour', path_to_hour(data['filename']))

    # data.show(100)
    # tmp = data.select('filename')
    # tmp.show(20, False)

    # data = data.cache()
    # real    0m7.858s
    # user    0m20.414s
    # sys     0m1.731s


    data = data.filter(data['language']=='en')
    data = data.filter(data['title']!='Main_Page')
    data = data.drop(data['title'].startswith('Special:'))

    data = data.cache()
    # real    0m7.268s
    # user    0m19.965s
    # sys     0m1.545s



    max_data = data.groupby('hour').max('time')
    data = data.join(max_data,'hour')

    # data = data.cache()
    # real    0m8.450s
    # user    0m21.542s
    # sys     0m1.902s

    
    data = data[data['time']==data['max(time)']].select('hour','title','time')
    data = data.sort(data['hour'],data['title'])
    
    # data.show(100, False)
    # data = data.cache()

    data = data.write.csv(out_directory, mode='overwrite')

if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)

