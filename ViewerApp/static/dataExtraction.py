from classes import db, User
from collections import defaultdict
from datetime import datetime

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
        info = ConsumptionInfo(time, user.energy, user.treesKilled, user.cost)
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


print(getDevices("Isaac"))