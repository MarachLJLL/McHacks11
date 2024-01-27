from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))

class DP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(100))
    time = db.Column(db.DateTime)
    energy = db.Column(db.Float)


