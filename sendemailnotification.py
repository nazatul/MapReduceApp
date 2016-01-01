import smtplib

from_addr=''
cc_addr_list=()
username=''
password=''
smtpserver='smtp.gmail.com:587'

def sendemail(to_addr_list,subject,message):
	header = 'From: %s\n' % from_addr
	header += 'To: %s\n' % ','.join(to_addr_list)
	header += 'Cc: %s\n' % ','.join(cc_addr_list)
	header += 'Subject: %s\n \n' % subject
	message=header+"\n"+message
	server=smtplib.SMTP(smtpserver)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(username,password)
	print message
	problems=server.sendmail(from_addr,to_addr_list,message)
	server.quit()
