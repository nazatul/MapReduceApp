# MapReduceApp built using Amazon-AWS

An application that allows users to submit MapReduce jobs for Data Analysis. The application is deployed on the Amazon Web Services, using Django to provide the MVC framework, EC2 instance for deployment, S3 for scalable storage, SQS for queuing jobs and EMR to perform the Map Reduce Job (this uses Hadoop framework for analytics).

-Place this in your Django project created in your Amazon AWS account.
-Create queue mapreducequeue in your SQS account.
-Upload tasks from web-interface and run consumerprogram.py to execute the jobs(from the terminal).
-Create S3 Bucket mapreduceapp/uploadedfiles and in it place the files:
    -wordCountMapper.py
    -wordCountReducer.py
    -invertedindexMapper.py
    -invertedindexReducer.py

Change the following items:

In sendemailnotification.py:
Add from_addr, username, password of your email account.

In consumerprogram.py:
Add access_key, secret_key and region of your Amazon AWS account.

In MapReduceApp/views.py:
Add access_key, secret_key and region of your Amazon AWS account.
