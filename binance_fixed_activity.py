import sys
import requests
import json
import config  # stores all keys
from time import time
import hmac
import hashlib
from pprint import pprint
import telegrambot
import datetime

print("\nRunning script at {} ...".format(datetime.datetime.now()), '\n')


rootDir = '/root/SnipeFixed/'

# load historical data
oldProjects = []
historyfile = rootDir + 'history_activity.json'
with open(historyfile, 'r') as myfile:
    data = myfile.read()
if len(data) > 0:
    olddata = json.loads(data)
else:
    olddata = ''

# print("olddata from file:")
# print(olddata)
# print()
# temp = {'asset': 'asdf', 'type': 'ACTIVITY', 'duration': 21, 'interestRate': '0.2', 'lotSize': '100', 'lotsLowLimit': 0, 'lotsPurchased': 100000, 'lotsUpLimit': 100000, 'maxLotsPerUser': 5000,
#         'projectId': 'HNKN21DAYSS002K', 'projectName': 'NKN 21D (20%)', 'status': 'PRE_REDEMPTION', 'interestPerLot': '1.1506', 'needKyc': False, 'withAreaLimitation': False, 'displayPriority': -12, 'date_added': '2021-04-16'}
# olddata.append(temp)
# pprint(olddata)
# sys.exit()

today = datetime.date.today()
for item in olddata:
    date_added = datetime.date.fromisoformat(item['date_added'])
    deletestring = ''
    t = today - date_added
    timediff = int(t.days)

    #print("timediff: {}  | duration: {}  ".format(timediff, item['duration']))

    # only track non-expired items in list oldProjects. Flag the expired ones.
    if timediff <= item['duration']:
        oldProjects.append(item['projectId'])
        item['expired'] = 'NO'

# Filter out expired items. Only keep non expired ones.
olddata = [x for x in olddata if x['expired'] == 'NO']


# ------------Fetch data from Binance -----------------------------------------
# get APIkeys from config.py
api_key = config.api_key
api_secret = config.api_secret


def hashing(query_string):  # sha256 hash function to create signature needed for binance. Refer to this url for more info
    # https://github.com/binance-exchange/binance-signature-examples/blob/master/python/signature.py
    return hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()


baseurl = 'https://api.binance.com'
queryurl = baseurl + '/sapi/v1/lending/project/list?'


t = time()
timestamp = int(t*1000)
query_timestamp = 'timestamp=' + str(timestamp)

# all query paramaters + timestamp. This all together is used to create signature
query_parameters = 'type=ACTIVITY&status=ALL&isSortAsc=true&sortBy=START_TIME&current=1&size=100&' + query_timestamp

# create signature & final URl to request
signature = hashing(query_parameters)
signedurl = queryurl + query_parameters + '&signature=' + signature

# request header must include api_key
header = {'X-MBX-APIKEY': api_key}

# request
resp = requests.get(signedurl, headers=header)
# ---------------data received from binance ------------------------


# clean up results
results = resp.json()   # target_assets = ('BTC', 'ALICE', 'FOR')

# filter results by status (only purchasing and preredemption are valid)
valid_results = [x for x in results if  # x['asset'] in target_assets and
                 x['status'] in ('PURCHASING', 'PRE_REDEMPTION')
                 # and x['projectId'] not in oldProjects
                 ]
print('num of items retrieved from binance: ', len(valid_results))

# loop through valid results,  identify new items
today = datetime.date.today()

printstr = ''
newitems = ''
newItemCount = 0
if len(valid_results) > 0:
    for item in valid_results:
        # single string containing summary of all data
        printstr = printstr + '{} | duration: {} | APY: {} | lotSize: {} | projectId: {}'.format(
            item['asset'], item['duration'], item['interestRate'], item['lotSize'], item['projectId']) + '\n'

        # detect new item and add them to our list of old items
        if item['projectId'] not in oldProjects:
            item['date_added'] = today.strftime('%Y-%m-%d')
            newitems = newitems + \
                '{}  |  projectId: {} '.format(
                    item['asset'], item['projectId']) + '\n'
            newItemCount = newItemCount+1

            # add new item to olddata, with today's date written into "date_added"
            olddata.append(item)
    # end loop
    print(printstr)

    print("Number of new items: ", newItemCount)

    if newItemCount > 0:  # if new items were detected, then alert via telegram

        telegram_msg = 'New items detected: \n' + newitems + \
            '\n\n All active activities: \n' + printstr
        print('sending message....')

        telegrambot.telegram_bot_sendtext(telegram_msg)
    else:
        print("no need to message telegram")

    print('-----done-------')

with open(historyfile, 'w') as fout:
    json.dump(olddata, fout)

msg = 'finished running bot. Fetched these from binance: ' + \
    str(newItemCount) + '\n' + printstr
