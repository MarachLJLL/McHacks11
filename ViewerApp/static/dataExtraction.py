from classes import db, User, ConsumptionInfo
from collections import defaultdict
from datetime import datetime
from flask import current_app

def getDevices(user):
    """
    return dictionary: {
     device name:[consumption_info,]
    }
    """
    devices = defaultdict(list)
    users = User.query.filter_by(name=user).all()

    for user in users:
        time = convertTimeToDatetime(user.time)
        info = ConsumptionInfo(time, user.energy, user.trees_killed, user.cost)
        devices[user.device_id].append(info)

    # get all entries for this user
    # have a Counter() for all of the devices
    # set devicesList to the keys of the Counter()
    return devices

def convertTimeToDatetime(time):
    timestamp = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
    year = timestamp.year
    month = timestamp.month
    day =  timestamp.day
    hour = timestamp.hour
    minute = timestamp.minute
    return datetime(year=year, month=month, day=day, hour=hour, minute=minute)
