from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100)) 
    
class EnergyConsumption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    consumption = db.Column(db.Float)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    energy_consumptions = db.relationship('EnergyConsumption', backref='device', lazy=True)