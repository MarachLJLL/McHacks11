from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    device_id = db.Column(db.String(100))
    time = db.Column(db.String(100))
    energy = db.Column(db.Float)
    trees_killed = db.Column(db.Float)
    cost = db.Column(db.Float)

# timestamp, kWHours, treesKilled, costDollars, userId (device id)
class ConsumptionInfo():
    def __init__(self, time, kwh, treesKilled, cost):
        self.time = time #datetime
        self.kwh = kwh #float
        self.treesKilled = treesKilled #float
        self.cost = cost #float
        
    


