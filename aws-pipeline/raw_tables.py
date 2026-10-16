from pyspark import pipelines as dp 
from pyspark.sql.functions import *
for i in dbutils.fs.ls('s3://de-prj/csv_files'):
    if not i.name.endswith('.csv'):
        continue
    table_name=i.name.split('.')[0]
    def create_table(table_name=table_name, file_name=i.name):
        @dp.table(name=f"bronze_{table_name}")
        def tbl():
            return(
                spark.readStream.format('cloudFiles').option('cloudFiles.format','csv') \
                    .option('header','true').option('cloudFiles.inferColumnTypes','true') \
                    .option('pathGlobFilter', file_name) \
                    .load('s3://de-prj/csv_files') \
                    .withColumn('ingested_time',current_timestamp())
            )
            
        return tbl 
    create_table()
    