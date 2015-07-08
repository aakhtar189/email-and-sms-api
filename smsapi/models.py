import datetime
from flask import url_for
from tasks import db


class Sms(db.Document):
    message = db.StringField(max_length=255, required=True)
    message_type = db.StringField(max_length=255, required=True)
    mobile = db.ListField()