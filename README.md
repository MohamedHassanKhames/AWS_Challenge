# AWS challenge
  
In this challenge, you’ll be ingesting data from an API of your choosing into AWS. The data should be ingested on a cadence that aligns to the frequency of changes in the data.    

### Assumptions
- Assuming lambda functions zip and glue job code will  be stored in a S3 bucket
- For better illustration of the partition process I choose 7 minutes as a frequencey period.
- Partitioning will be based on datetime - Year/Month/Day/Hour/Minute, just for illustration purposes.
- I've added the partitioning part as an event-based architecture, just for illustration. However, I know that it is not the best option and it should be created as a batch job for better performance and cost optmization.

### Architecture

  ![IMAGE_DESCRIPTION](https://images-for-aws-challenge.s3.amazonaws.com/design.png)
  
### Step 
- First, you will need to create a S3 bucket to store the lambda and glue job code files including
    - lambda_function.zip
    - lambda_glue.zip
    - glue_job.py
- Import the cloudformation.yaml file into AWS Stack as shown:
  ![IMAGE_DESCRIPTION](https://images-for-aws-challenge.s3.amazonaws.com/1.png)
- Enter stack name and the all required parameters - ***provided in the next section*** - as shown: 
  ![IMAGE_DESCRIPTION](https://images-for-aws-challenge.s3.amazonaws.com/2.png)
- Provide the appropriate IAMRole for cloudfomration to run the stack and create the appropriate resources.
  ![IMAGE_DESCRIPTION](https://images-for-aws-challenge.s3.amazonaws.com/3.png)
- Finally, acknowledge and sumbit.
  ![IMAGE_DESCRIPTION](https://images-for-aws-challenge.s3.amazonaws.com/4.png)
- Now you can check the created resources and the files being uploaded into your newly created buckets.  
     
  
#### Parameters 

- **LambdaCodeS3Bucket** : This is the s3 bucket where you will upload all source code. 
    - **Must be Unique**
    - Examlpe: aws-challenge-ingestion-bucket-code
- **GlueScriptS3Path** : This is a complete link for glue_job.py script
    - Examlpe:   s3://aws-challenge-ingestion-bucket-code/glue_job.py
- **LambdaAPICodeS3Key** : This is the zip file name for API lambda inside S3 bucket
  -  Examlpe: lambda_function.zip
- **LambdaGlueCodeS3Key** : This is the zip file name for Glue lambda inside S3 bucket
  -  Examlpe: lambda_glue.zip
- **NonPartitionedS3BucketName** : This is the S3 Staging bucket "Non-partionined"
  -  Examlpe: aws-challenge-non-partitioned-bucket
- **PartitionedS3BucketName** : This is the final target, the partitioned S3 bucket
  - Examlpe: aws-challenge-partitioned-bucket
- **LambdaAPIName** : This is the lambda function responisble for calling the weather API.
  - Example: weatherAPI
- **LambdaGlueName** : This is the lambda function which will be notified by s3 and will initiate the glue job for partitioning.
  - Example: glueLambda
- **GlueJobNameP** : This is the glue job for partitioning the data.
  - Example: glueJob

> Note: `if you tried to delete the stack after finishing, you will face an error when deleting the buckets since it will not be empty and you will need to do it manually. `  
