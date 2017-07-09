import requests
import datetime
import untangle
import time
import sys
from intake.models import Generated
from requests.auth import HTTPDigestAuth

TIMESTEP = datetime.timedelta(days=30)

def recurse_save(group, model):
    mid = int(len(group) / 2)

    try:
        model.objects.bulk_create(group)
    except:
        try:
            model.objects.bulk_create(group[:mid])
        except:
            if mid >= 1:
                recurse_save(group[:mid], model)
            elif len(group) == 1:
                print("Error saving " + str(group[0].timestamp))

        try:
            model.objects.bulk_create(group[mid:])
        except:
            if mid >= 1:
                recurse_save(group[mid:], model)
            elif len(group) == 1:
                print("Error saving " + str(group[mid].timestamp))

def get_epoch(endpoint):
    username = endpoint.credential.username
    password = endpoint.credential.password
    url = endpoint.url.format(begin=time.time(), end=time.time())

    response = requests.get(url, auth=HTTPDigestAuth(username, password))

    page = untangle.parse(response.text)
    print(url)

    epoch = int(page.group.data["epoch"], 16)
    endpoint.last_retrieved = datetime.datetime.fromtimestamp(epoch, endpoint.timezone)
    endpoint.save()

def get(endpoint, current):
    if endpoint.last_retrieved is None:
        get_epoch(endpoint)

    if current - endpoint.last_retrieved > TIMESTEP:
        print(str(current) + " is more than a day since the last timestamp, which is " + str(endpoint.last_retrieved) + ".")
        get(endpoint, current - TIMESTEP)

    endpoint.refresh_from_db()

    username = endpoint.credential.username
    password = endpoint.credential.password
    end = endpoint.last_retrieved

    url = endpoint.url.format(begin=current.timestamp(), end=end.timestamp())

    response = requests.get(url, auth=HTTPDigestAuth(username, password))

    page = untangle.parse(response.text)

    try:
        data = [float(row.c[1].cdata) for row in page.group.data.r]
        
        time_delta = datetime.timedelta(seconds=int(page.group.data["time_delta"]))
        timestamp = datetime.datetime.fromtimestamp(int(page.group.data["time_stamp"], 16), endpoint.timezone)

        gens = []

        for i in range(1, len(data)):
            gens.append(Generated(
                value=data[i - 1] - data[i],
                timestamp=timestamp,
                sensor=endpoint))
            timestamp = timestamp - time_delta

        recurse_save(gens, Generated)
    except AttributeError:
        print('No data for ' + str(current) + '. Tried ' + url)
    
    endpoint.last_retrieved = current
    endpoint.save()

    print('Finished with day ' + str(current) + ' (' + str(Generated.objects.filter(sensor=endpoint).count()) + ')')
