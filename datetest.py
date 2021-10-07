import json
import datetime
from pprint import pprint

today = datetime.date.today()
print(today)

# read file. historical data.
with open('outputfile.json', 'r') as myfile:
    data = myfile.read()
olddata = json.loads(data)

oldProjects = []

for item in olddata:

    oldProjects.append(item['projectId'])

    date_added = datetime.date.fromisoformat(item['date_added'])
    deletestring = ''
    t = today - date_added
    timediff = int(t.days)

    # identify expired ones
    if timediff > item['duration']:
        deletestring = 'DELETE'
    # print("{}  |  added {}  |  duration: {}   |  timediff: {}  | {}".format(
    #     item['asset'], date_added, item['duration'], timediff, deletestring), '\n')


# new data. read inline for now:
newdata = [
    # already exists
    {
        "asset": "RIF",
        "type": "ACTIVITY",
        "duration": '28',
        "interestRate": "0.2",
        "lotSize": "100",
        "lotsLowLimit": '0',
        "lotsPurchased": '41290',
        "lotsUpLimit": '50000',
        "maxLotsPerUser": '2500',
        "projectId": "HRIF28DAYSS012K",
        "projectName": "RIF 28D (20%)",
        "status": "PURCHASING",
        "interestPerLot": "1.5342",
        "needKyc": 'false',
        "withAreaLimitation": 'false',
        "displayPriority": '-15'
    },
    {
        "asset": "ZEC",
        "type": "ACTIVITY",
        "duration": '28',
        "interestRate": "0.2",
        "lotSize": "100",
        "lotsLowLimit": '0',
        "lotsPurchased": '41290',
        "lotsUpLimit": '50000',
        "maxLotsPerUser": '2500',
        "projectId": "ZEC123456",
        "projectName": "ZEC 20%",
        "status": "PURCHASING",
        "interestPerLot": "1.5342",
        "needKyc": 'false',
        "withAreaLimitation": 'false',
        "displayPriority": '-15'
    }
]

for item in newdata:
    detectednew = ''
    if item['projectId'] not in oldProjects:
        detectednew = 'NEW'
        # print(item['projectId'])
    print('{}  |  projectId: {}   |  {}'.format(
        item['asset'], item['projectId'], detectednew))

print()


print(oldProjects)
