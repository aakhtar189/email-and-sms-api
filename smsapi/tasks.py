from celery import Celery
from flask import Flask
from urllib2 import Request, urlopen, URLError
from urllib import urlencode
import json
from flask.ext.mongoengine import MongoEngine

apps = Flask(__name__)

apps.config["MONGODB_SETTINGS"] = {'DB': "my_sms_db"}
apps.config["SECRET_KEY"] = "KeepThisS3cr3t"

db = MongoEngine(apps)

from models import Sms

from redis import Redis
redis = Redis()

celery = Celery('tasks')
celery.config_from_object('celeryconfig')

@celery.task
def sms_list_data():
	val = redis.rpop("sms_list")
	while(val is not None) :
		json_obj = json.loads(val)
		mobile_no = json_obj['mobile_no']
		if type(mobile_no) is unicode:
			mobile_no = mobile_no.split(',')
		message_type = json_obj['message_type']
		message = json_obj['message']
		
		send_sms(mobile_no, message)
		
		s = Sms(message=message,message_type = message_type, mobile = mobile_no)
		s.save()

		val = redis.rpop("sms_list")

	return val


def send_sms(mobile_no, message):
	
	text_message = {'text': message}
	message = urlencode(text_message)
	for mobile in mobile_no:
		sms_url = 'https://rest.nexmo.com/sms/xml?api_key=d346ac6a&api_secret=acd49d23p&to=' + mobile + '&from=asif&type=text&text=' + message
		# sms_url = 'https://rest.nexmo.com/sms/xml?api_key=d346ac6a&api_secret=acd49d23p&to=' + mobile + '&' + message
		request = Request(sms_url)
		try:
			response = urlopen(request)
			received_response = response.read()
			print received_response	
		except URLError, e:
			print 'Got an error code:', e

