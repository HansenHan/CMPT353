import sys
from pyspark.sql import SparkSession, functions, types, Row
import re
import math
spark = SparkSession.builder.appName('correlate logs').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

line_re = re.compile(r"^(\S+) - - \[\S+ [+-]\d+\] \"[A-Z]+ \S+ HTTP/\d\.\d\" \d+ (\d+)$")


def line_to_row(line):
    """
    Take a logfile line and return a Row object with hostname and bytes transferred. Return None if regex doesn't match.
    """
    m = line_re.match(line)
    if m:
        # TODO
        return Row(hostname=m.group(1),bytes=float(m.group(2)))
    else:
        return None


def not_none(row):
    """
    Is this None? Hint: .filter() with it.
    """
    return row is not None


def create_row_rdd(in_directory):
    log_lines = spark.sparkContext.textFile(in_directory)
    # TODO: return an RDD of Row() objects
    log_lines = log_lines.map(line_to_row)
    log_lines = log_lines.filter(not_none)
    return log_lines


def main(in_directory):
    logs = spark.createDataFrame(create_row_rdd(in_directory))
    # logs.show()
    # TODO: calculate r.
    counts = logs.groupby('hostname').count().cache()
    sumb = logs.groupby('hostname').sum('bytes').cache()
    group = sumb.join(counts, 'hostname')

    # group.show()

    group = group.withColumnRenamed('count', 'xi')
    group = group.withColumnRenamed('sum(bytes)', 'yi')
    group = group.withColumn('xi2', group['xi']**2)
    group = group.withColumn('yi2', group['yi']**2)
    group = group.withColumn('xiyi', group['xi']*group['yi'])

    # group.show()

    result = group.groupby().sum()
    n = group.count()
    # print(n)
    # result.show()

    result = result.first()

    xi = result[1]
    yi = result[0]
    xi2 = result[2]
    yi2 = result[3]
    xiyi = result[4]

    r = (n*xiyi - xi*yi)/(math.sqrt(n*xi2 - xi**2)*math.sqrt(n*yi2 - yi**2)) # TODO: it isn't zero.
    print("r = %g\nr^2 = %g" % (r, r**2))


if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)
