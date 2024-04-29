import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import gs_derived

args = getResolvedOptions(sys.argv, ['JOB_NAME','nonPartitionedBucketName','partitionedBucketName','fileName'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args) 
logger = glueContext.get_logger()  

# Just to specify only the added file as a part of the automation.
source_s3_path =  "s3://" + args['nonPartitionedBucketName'] + "/" +args['fileName']
target_s3_path =  "s3://" + args['partitionedBucketName'] 
logger.info("==================================")
logger.info("source_s3_path" + source_s3_path)
logger.info("==================================")
logger.info("target_s3_path" + target_s3_path)
logger.info("==================================")

AmazonS3_node1714317723195 = glueContext.create_dynamic_frame.from_options(format_options={"multiline": False}, 
                             connection_type="s3", format="json", connection_options={"paths": [source_s3_path], "recurse": True}, transformation_ctx="AmazonS3_node1714317723195")

DerivedYear= AmazonS3_node1714317723195.gs_derived(colName="year", expr="year(location.localtime)")
DerivedMonth = DerivedYear.gs_derived(colName="month", expr="month(location.localtime)")
DerivedDay = DerivedMonth.gs_derived(colName="day", expr="day(location.localtime)")
DerivedHour = DerivedDay.gs_derived(colName="hour", expr="hour(location.localtime)")
DerivedMin = DerivedHour.gs_derived(colName="minute", expr="minute(location.localtime)")
 
AmazonS3_node1714317856429 = glueContext.write_dynamic_frame.from_options(frame=DerivedMin, 
                            connection_type="s3", format="glueparquet", connection_options={"path": target_s3_path, "partitionKeys": ["yearColumn", "monthColumn", "dayColumn"]}, 
                            format_options={"compression": "snappy"}, transformation_ctx="AmazonS3_node1714317856429")

job.commit()