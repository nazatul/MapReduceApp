from django.shortcuts import render_to_response
from django.template import RequestContext
from MapReduce.forms import UploadFileForm
from MapReduce.forms import UploadMapForm
from MapReduce.forms import UploadReduceForm
import cPickle
import boto.sqs
import boto.s3
import os
from boto.sqs.message import Message

ACCESS_KEY=""
SECRET_KEY=""
REGION=""

def percent_cb(complete,total):
	print('.')

def upload_to_s3_bucket_path(bucketname,path,filename):
	conn=boto.connect_s3(ACCESS_KEY,SECRET_KEY)
	mybucket=conn.get_bucket(bucketname)
	fullkeyname=path+"/"+filename
	key=mybucket.new_key(fullkeyname)
	key.set_contents_from_filename(filename,cb=percent_cb,num_cb=10)

def handle_uploaded_file(f):
	uploadfilename=os.path.dirname(os.path.dirname(__file__))+'/MapReduceApp/'+f.name
	with open(uploadfilename,'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
	return uploadfilename

def enqueuejob(datafile,mapper,reducer,emailaddress):
	conn=boto.sqs.connect_to_region(REGION,aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
	queue_name='mapreducequeue'
	q=conn.get_all_queues(prefix=queue_name)
	msgdict={'datafile':datafile,'mapper':mapper,'reducer':reducer,'emailaddress':emailaddress}
	msg=cPickle.dumps(msgdict)
	m=Message()
	m.set_body(msg)
	status=q[0].write(m)

def createjob(datafilename,mapfilename,reducefilename,mapreduceprogram,emailaddress):
	upload_to_s3_bucket_path('mapreduceapp','uploadedfiles',datafilename)
	datafilename='s3n://mapreduceapp/uploadedfiles'+datafilename
	if mapreduceprogram=='wordcount':
		mapper='s3n://mapreduceapp/uploadedfiles/wordCountMapper.py'
		reducer='s3n://mapreduceapp/uploadedfiles/wordCountReducer.py'
	elif mapreduceprogram=='invertedindex':
		mapper='s3n://mapreduceapp/uploadedfiles/invertedindexMapper.py'
		reducer='s3n://mapreduceapp/uploadedfiles/invertedindexucer.py'
	else:
		upload_to_s3_bucket_path('mapreduceapp','uploadedfiles',mapfilename)
		upload_to_s3_bucket_path('mapreduceapp','uploadedfiles',reducefilename)
		mapper='s3n://mapreduceapp/uploadedfiles'+mapfilename
		reducer='s3n://mapreduceapp/uploadedfiles'+reducefilename
	enqueuejob(datafilename,mapper,reducer,emailaddress)
	return datafilename,mapper,reducer,emailaddress

def home(request):
	if request.method=='POST':
		datafilename=''
		mapfilename=''
		reducefilename=''
		mapreduceprogram=''
		form=UploadFileForm(request.POST,request.FILES)
		if form.is_valid():
			datafilename=handle_uploaded_file(request.FILES.get('myfilefield'))
		mapform=UploadMapForm(request.POST,request.FILES)
		if mapform.is_valid():
			mapfilename=handle_uploaded_file(request.FILES('mymapfield'))	
		reduceform=UploadReduceForm(request.POST,request.FILES)
		if reduceform.is_valid():
			reducefilename=handle_uploaded_file(request.FILES('myreducefield'))
		emailaddress=request.POST.get('email')		
		mapreduceprogram=request.POST.get('mapreduceprogram')
		datafile,mapper,reducer,emailaddress=createjob(datafilename,mapfilename,reducefilename,mapreduceprogram,emailaddress)
		return render_to_response('process.html',{'datafile':datafile,'mapper':mapper,'reducer':reducer,
			'emailaddress':emailaddress},context_instance=RequestContext(request))
	else:
		form=UploadFileForm()
		mapform=UploadMapForm()
		reduceform=UploadReduceForm()
		return render_to_response('index.html',{'form':form,'mapform':mapform,'reduceform':reduceform},
			context_instance=RequestContext(request))	
