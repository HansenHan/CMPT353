import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('reddit relative scores').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

comments_schema = types.StructType([
    types.StructField('archived', types.BooleanType()),
    types.StructField('author', types.StringType()),
    types.StructField('author_flair_css_class', types.StringType()),
    types.StructField('author_flair_text', types.StringType()),
    types.StructField('body', types.StringType()),
    types.StructField('controversiality', types.LongType()),
    types.StructField('created_utc', types.StringType()),
    types.StructField('distinguished', types.StringType()),
    types.StructField('downs', types.LongType()),
    types.StructField('edited', types.StringType()),
    types.StructField('gilded', types.LongType()),
    types.StructField('id', types.StringType()),
    types.StructField('link_id', types.StringType()),
    types.StructField('name', types.StringType()),
    types.StructField('parent_id', types.StringType()),
    types.StructField('retrieved_on', types.LongType()),
    types.StructField('score', types.LongType()),
    types.StructField('score_hidden', types.BooleanType()),
    types.StructField('subreddit', types.StringType()),
    types.StructField('subreddit_id', types.StringType()),
    types.StructField('ups', types.LongType()),
    #types.StructField('year', types.IntegerType()),
    #types.StructField('month', types.IntegerType()),
])


def main(in_directory, out_directory):
    comments = spark.read.json(in_directory, schema=comments_schema)
# real    0m5.799s
# user    0m17.531s
# sys     0m0.937s

    comments.cache()
# real    0m5.812s
# user    0m18.207s
# sys     0m1.031s



    # comments.show()

    # TODO

    averages = comments.groupby('subreddit').avg()
    # averages = averages.cache()
# real    0m6.646s
# user    0m19.839s
# sys     0m1.113s

    averages = averages.drop(averages['subreddit']<=0)
    # averages.cache()
# real    0m6.298s
# user    0m19.205s
# sys     0m0.976s


    # averages.show()

    averages = averages.select('subreddit', 'avg(score)')

    # averages.show()

    # averages = functions.broadcast(averages)
    comments_1 = comments.join(averages, 'subreddit')
    # comments_1.cache()
# real    0m5.996s
# user    0m18.717s
# sys     0m0.977s


    # comments_1.show()

    comments_1 = comments_1.withColumn('relative_score', comments_1['score']/comments_1['avg(score)'])

    # comments_1.show()

    max_relative = comments_1.groupby('subreddit').max('relative_score')
    max_relative.cache()
# real    0m6.564s
# user    0m20.518s
# sys     0m1.100s


    # max_relative.show()

    max_relative = max_relative.withColumnRenamed('subreddit', 'reddit_max')

    # max_relative.show()

    # max_relative = functions.broadcast(max_relative)
    best_author = comments_1.join(max_relative, max_relative['max(relative_score)'] == comments_1['relative_score'])
    # best_author.cache()
# real    0m5.855s
# user    0m18.708s
# sys     0m0.825s


    # best_author.show()

    best_author = best_author.select('subreddit', 'author', 'max(relative_score)')
    best_author = best_author.withColumnRenamed('max(relative_score)', 'rel_score')
    best_author = best_author.sort(best_author['subreddit'])

    # best_author.show()

    best_author.write.json(out_directory, mode='overwrite')


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)
