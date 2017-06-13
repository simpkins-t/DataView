from django.db import models
from requests.auth import HTTPDigestAuth
import requests
import untangle

class SensorSite(models.Model):
    name = models.CharField(max_length=50)

class Credential(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

class SensorEndpoint(models.Model):
    url = models.URLField()
    credential = models.ForeignKey("Credential")
    site = models.ForeignKey("SensorSite")
    # Mountain Time -- should store timezone and use that in parsing

    def get(self, start, end):
        username = self.credential.username
        password = self.credential.password
        url = self.url.format(start=start, end=end)

        response = requests.get(url, auth=HTTPDigestAuth(username, password))

        page = untangle.parse(response.text)

        data = [float(row.c[1].cdata) for row in page.group.data.r]
        
        time_delta = int(page.group.data["time_delta"], 16)
        timestamp = int(page.group.data["time_stamp"], 16) # Make TZ aware

        deltas = []
            
        for i in range(1, len(data)):
            deltas.append({
                'value': data[i - 1] - data[i],
                'timestamp': timestamp
                })
            timestamp = timestamp - time_delta


        return deltas

class Generated(models.Model):
    value = models.FloatField()
    timestamp = models.DateTimeField()
    sensor = models.ForeignKey("SensorEndpoint")
