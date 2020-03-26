import sys
from pyspark.sql import SparkSession, functions, types
# from pyspark.sql.functions import col

spark = SparkSession.builder.appName('wikipedia popular').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

schema1 = types.StructType([
    types.StructField('lang', types.StringType()),
    types.StructField('content', types.StringType()),
    types.StructField('times', types.IntegerType()),
    types.StructField('bytes', types.IntegerType()),
])

def input_file_name(in_directory):
    return spark.read.csv(in_directory, schema = schema1, sep = ' ').withColumn('filename', functions.input_file_name())


# udf: user defined function
# cool cool cool. spent 5 mins to calculate the scope of the string length
def path_to_hour(path):
    filename = path.split('/')[-1]
    return filename[11:22]


def main():
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    
    wiki = input_file_name(in_directory)
    # wiki.show(20, False)   # Note that "False" means to show the completed content 
    path_to_hour1 = functions.udf(path_to_hour, returnType=types.StringType())
    wiki = wiki.withColumn('111', path_to_hour1(functions.input_file_name()))
    wiki = wiki.drop('filename')
    wiki = wiki.withColumnRenamed('111', 'filename')
    # wiki.show()

    # begin to filter:
    wiki = wiki.filter(wiki.lang.like('en'))
    wiki = wiki.filter(wiki['content'] != 'Main_Page') 
    wiki = wiki.filter(wiki['content'].startswith('Special:') != True)
    wiki = wiki.cache()

    temp = wiki.groupBy('filename').max('times')
    temp = temp.withColumnRenamed('filename', 'name')
    # temp.show()
    final = wiki.join(temp, on=((wiki['times'] == temp['max(times)']) & (wiki['filename'] == temp['name']))) 
    final = final.select('filename', 'content', 'times')

    final = final.sort('filename', 'content')
    # final.show()


    # without .cache():
    # real	0m20.369s
    # user	0m28.471s
    # sys	0m1.355s



    # with .cache():
    # real	0m17.204s
    # user	0m28.023s
    # sys	0m1.123s


    final.write.csv(out_directory, mode='overwrite')

if __name__=='__main__':
    main()












