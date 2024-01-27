from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    devices = db.Column(db.JSON)

class Device(db.Model):
    device_id = db.Column(db.String(100))
    expenditure_entries = db.Column(db.ExpenditureEntry(1000))

class ExpenditureEntry(db.Model):
    time = db.Column(db.datetime(100))
    energy = db.Column(db.Float(100))


