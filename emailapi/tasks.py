from celery import Celery
from flask import Flask
from urllib2 import Request, urlopen, URLError
from urllib import urlencode
from flask.ext.mongoengine import MongoEngine
from flask_mail import Mail, Message
import json

apps = Flask(__name__)
mail=Mail(apps)

apps.config["MONGODB_SETTINGS"] = {'DB': "my_email_db"}
apps.config["SECRET_KEY"] = "KeepThisS3cr3t"

db = MongoEngine(apps)

from models import Email

from redis import Redis
redis = Redis()

celery = Celery('tasks')
celery.config_from_object('celeryconfig')

@celery.task
def email_list_data():
	with apps.app_context():

		val = redis.rpop("email_list")
		
		while(val is not None):
			
			json_obj = json.loads(val)
			email_from = json_obj['email_from']
			email_to = json_obj['email_to']
		
			if type(email_to) is unicode:
				email_to = email_to.split(',')

			email_subject = json_obj['email_subject']
			email_body = json_obj['email_body']
			email_type = json_obj['email_type']
			email_password = json_obj['email_password']

			apps.config.update(
			DEBUG=True,
			#EMAIL SETTINGS
			MAIL_SERVER='smtp.gmail.com',
			MAIL_PORT=465,
			MAIL_USE_SSL=True,
			MAIL_USERNAME = email_from,
			MAIL_PASSWORD = email_password
			)
		
			mail=Mail(apps)
			send_email(email_subject,email_from, email_password, email_body, email_to)
			
			em = Email(email_subject = email_subject, email_to = email_to, 
				email_from = email_from, email_body = email_body, email_type = email_type)
			em.save()

			val = redis.rpop("email_list")


		return 0

def send_email(email_subject, email_from, email_password, email_body, email_to) :

	msg = Message(
              email_subject,
	       sender=email_from,
	       recipients=
               email_to)
	msg.body = email_body
	mail.send(msg)
	return "Sent"