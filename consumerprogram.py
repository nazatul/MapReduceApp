import boto.sqs
from boto.sqs.message import Message
import cPickle
import boto.emr
from boto.emr.step import StreamingStep
import time
from sendemailnotification import sendemail

ACCESS_KEY=""
SECRET_KEY=""
REGION=""

def sendnotification(msg,status,downloadlink):
	receipients_list=[msg['emailaddress']]
	subject= 'MapReduce Job Notification'
	print downloadlink
	message="Your MapReduce Job is complete. Downloading results from: "+downloadlink
  	sendemail(receipients_list,subject,message)

def createemrjob(msg):
	print "Connecting to EMR"
	conn=boto.emr.connect_to_region(REGION,aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
	print"Creating streaming step"
	t=time.localtime(time.time())
	job_datetime=str(t.tm_year)+str(t.tm_mon)+str(t.tm_mday)+str(t.tm_hour)+str(t.tm_min)+str(t.tm_sec)
	outputlocation='s3n://mapreduceapp/uploadedfiles/'+job_datetime
	step=StreamingStep(name=job_datetime,mapper=msg['mapper'],reducer=msg['reducer'],input=msg['datafile'],output=outputlocation)
	print"Creating job flow"
	jobid=conn.run_jobflow(name=job_datetime,log_uri='s3n://mapreduceapp/uploadedfiles/logs',steps=[step],ami_version="2.4.9",
	job_flow_role="EMR_EC2_DefaultRole",service_role="EMR_DefaultRole")
	print"Submitted job flow"
	print"Waiting for job flow to complete"
	status=conn.describe_cluster(jobid)
	print status.status.state
	while status.status.state=='STARTING' or status.status.state=='RUNNING' or status.status.state=='WAITING' or status.status.state=='SHUTTING_DOWN':
		time.sleep(5)
		status=conn.describe_cluster(jobid)
	print"Job status: " +str(status.status.state)
	print"Completed Job: "+job_datetime
	downloadlink='http://mapreduceapp.s3-website-us-west-2.amazonaws.com/uploadedfiles/'+job_datetime+'/part-00000'
	sendnotification(msg,status.status.state,downloadlink)

print"Connecting to SQS"
conn=boto.sqs.connect_to_region(REGION,aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
queue_name='mapreducequeue'
print"Connecting to queue: "+queue_name
q=conn.get_all_queues(prefix=queue_name)
count=q[0].count()
print"Total message in queue: "+str(count)
print"Reading message from queue"
for i in range(count):
	m=q[0].read()
	m.get_body()
	msg=cPickle.loads(str(m.get_body()))
	print"Message %d: %s"%(i+1,msg)
	createemrjob(msg)
	q[0].delete_message(m)
print"Read %d messages from queue "%(count)
