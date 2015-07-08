import datetime
from flask import url_for
from tasks import db


class Email(db.Document):
    email_subject =  db.StringField(max_length=255, required=True)
    email_body = db.StringField(max_length=4000, required=True)
    email_type = db.StringField(max_length=255, required=True)
    email_to = db.ListField()
    email_from = db.StringField(max_length=255, required=True)