from django.db import models
from timezone_field import TimeZoneField
from django.db.models import Min, Max
import datetime
import json
import pytz
import time


class SensorSite(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    description = models.TextField()
    timezone = TimeZoneField(default='US/Hawaii')

    def sensor_count(self):
        return SensorEndpoint.objects.filter(site=self).count()

class Credential(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

class SensorEndpoint(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()
    credential = models.ForeignKey("Credential")
    site = models.ForeignKey("SensorSite")
    last_retrieved = models.DateTimeField(blank=True, null=True)
    timezone = TimeZoneField(default='US/Mountain')

    def url_string(self):
        return self.url.split('/')[2]

    def last_day_coarse(self):
        return self.data_json(50, days=1)

    def last_hour(self):
        return self.data_json(hours=1)

    def generated_hour(self):
        return int(sum([o["generated"] for o in json.loads(self.data_json(hours=1))]))

    def count_hour(self):
        return len(json.loads(self.data_json(hours=1)))

    def last_day(self):
        return self.data_json(10, days=1)

    def generated_day(self):
        return int(sum([o["generated"] for o in json.loads(self.data_json(days=1))]))

    def count_day(self):
        return len(json.loads(self.data_json(days=1)))

    def last_week(self):
        return self.data_json(10, days=7)

    def generated_week(self):
        return int(sum([o["generated"] for o in json.loads(self.data_json(days=7))]))

    def count_week(self):
        return len(json.loads(self.data_json(days=7)))

    def last_month(self):
        return self.data_json(100, days=31)

    def generated_month(self):
        return int(sum([o["generated"] for o in json.loads(self.data_json(days=31))]))

    def count_month(self):
        return len(json.loads(self.data_json(days=31)))

    def last_3month(self):
        return self.data_json(100, days=31*3)

    def generated_3month(self):
        return int(sum([o["generated"] for o in json.loads(self.data_json(days=31*3))]))

    def count_3month(self):
        return len(json.loads(self.data_json(days=31*3)))

    def last_6month(self):
        return self.data_json(100, days=31*6)

    def generated_6month(self):
        return int(sum([o["generated"] for o in json.loads(self.data_json(days=31*6))]))

    def count_6month(self):
        return len(json.loads(self.data_json(days=31*6)))

    def last_year(self):
        return self.data_json(1000, days=365)

    def generated_year(self):
        return int(sum([o["generated"] for o in json.loads(self.data_json(days=365))]))

    def count_year(self):
        return len(json.loads(self.data_json(days=365)))

    def all_time(self):
        return self.data_json(1000, alltime=True)

    def generated_all_time(self):
        return int(sum([o["generated"] for o in json.loads(self.data_json(alltime=True))]))

    def count_hour(self):
        return len(json.loads(self.data_json(alltime=True)))

    def data_json(self, granularity=1, **time):
        try:
            if 'alltime' in time and time['alltime']:
                generateds = Generated.objects.filter(sensor=self)
            else:
                generateds = Generated.objects.filter(timestamp__gte=Generated.objects.filter(sensor=self).latest('timestamp').timestamp - datetime.timedelta(**time), sensor=self)
            return json.dumps([{
                "timestamp": generated.timestamp.strftime('%Y-%m-%dT%H:%M:%S'),
                "generated": generated.value
            } for generated in generateds[::granularity]])
        except:
            return "[]"
        
        

    def bounds(self):
        try:
            earliest = Generated.objects.filter(sensor=self).earliest('timestamp')
        except Generated.DoesNotExist:
            earliest = None
        
        try:
    
            latest = Generated.objects.filter(sensor=self).latest('timestamp')
        except Generated.DoesNotExist:
            latest = None

        return {
            'earliest': earliest.timestamp if earliest is not None else "No data",
            'latest': latest.timestamp if latest is not None else "No data"
        }

class Generated(models.Model):
    value = models.FloatField()
    timestamp = models.DateTimeField()
    sensor = models.ForeignKey("SensorEndpoint")

    class Meta:
        unique_together = ('timestamp', 'sensor', )
