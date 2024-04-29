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

# Just to specify only the added file as a part of the automation. However, it's better to run this job as a batch job at the end of the day for example for a better performance
source_s3_path =  "s3://" + args['nonPartitionedBucketName'] + "/" +args['fileName']
target_s3_path =  "s3://" + args['partitionedBucketName'] 
logger.info("========================hyeey==========")
logger.info("source_s3_path" + source_s3_path)
logger.info("========================hyeey==========")
logger.info("target_s3_path" + target_s3_path)
logger.info("========================hyeey==========")

# Script generated for node Amazon S3
AmazonS3_node1714317723195 = glueContext.create_dynamic_frame.from_options(format_options={"multiline": False}, 
                             connection_type="s3", format="json", connection_options={"paths": [source_s3_path], "recurse": True}, transformation_ctx="AmazonS3_node1714317723195")

# Script generated for node DerivedYear
DerivedYear_node1714318656608 = AmazonS3_node1714317723195.gs_derived(colName="yearColumn", expr="year(location.localtime)")

# Script generated for node DerivedMonth
DerivedMonth_node1714319059007 = DerivedYear_node1714318656608.gs_derived(colName="monthColumn", expr="month(location.localtime)")

# Script generated for node DerivedDay
DerivedDay_node1714319060375 = DerivedMonth_node1714319059007.gs_derived(colName="dayColumn", expr="day(location.localtime)")

# Script generated for node Amazon S3
AmazonS3_node1714317856429 = glueContext.write_dynamic_frame.from_options(frame=DerivedDay_node1714319060375, 
                            connection_type="s3", format="glueparquet", connection_options={"path": target_s3_path, "partitionKeys": ["yearColumn", "monthColumn", "dayColumn"]}, 
                            format_options={"compression": "snappy"}, transformation_ctx="AmazonS3_node1714317856429")

job.commit()