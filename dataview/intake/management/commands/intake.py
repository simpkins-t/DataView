from django.core.management.base import BaseCommand, CommandError
from intake.models import SensorEndpoint, Generated
import datetime

class Command(BaseCommand):
    help = 'Takes data in from sensors'    
    
    def add_arguments(self, parser):
        parser.add_argument('begin', nargs=1, type=int)
        parser.add_argument('end', nargs=1, type=int)

    def handle(self, *args, **options):
        begin = options['begin'][0]
        end = options['end'][0]
        endpoints = SensorEndpoint.objects.all()

        for endpoint in endpoints:
            data = endpoint.get(begin, end)
            
            print('Saving data...')
            for datum in data:
                timestamp = datetime.datetime.fromtimestamp(datum['timestamp'])
                value = datum['value']
                Generated.objects.create(timestamp=timestamp, value=value, sensor=endpoint)
