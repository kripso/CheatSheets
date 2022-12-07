from pyspark_utils import configure, transform_df, transform, Input, Output

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import Window as W
from pyspark.sql import types as T


SCHEMA = T.StructType(
    [
        T.StructField("_int", T.LongType()),
        T.StructField("_float", T.FloatType()),
        T.StructField("_string", T.StringType()),
        T.StructField("_date", T.DateType()),
        T.StructField("_array", T.ArrayType(T.LongType())),
        T.StructField(
            "_dict",
            T.StructType(
                [
                    T.StructField("int_key", T.LongType()),
                    T.StructField("string_key", T.StringType()),
                ]
            ),
        ),
        T.StructField(
            "_array_of_dict",
            T.ArrayType(
                T.StructType(
                    [
                        T.StructField("int_key", T.LongType()),
                        T.StructField("string_key", T.StringType()),
                    ]
                )
            ),
        ),
    ]
)


@configure()
@transform_df(
    Output("./data/example_2.json"),
    input_df=Input("./data/example.csv", SCHEMA),
)
def compute(df):

    df.printSchema()
    df.show(truncate=False)
    
    return df.coalesce(1)
