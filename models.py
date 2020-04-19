from . import db
from flask_login import UserMixin
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Cards(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    card_name = db.Column(db.String(128))
    card_number = db.Column(db.String(16))
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    cvv = db.Column(db.Integer)
    address = db.Column(db.String(500))
    used_on_google = db.Column(db.Boolean)
    used_on_amazon = db.Column(db.Boolean)
    used = db.Column(db.Boolean)
    usage = db.Column(db.String(128))
    amount = db.Column(db.Integer)
    expired = db.Column(db.Boolean)
    waste = db.Column(db.Boolean)
    in_progress = db.Column(db.Boolean)