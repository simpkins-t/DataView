from intake.models import SensorEndpoint, Generated
from intake.management.commands._private import get
from django.core.management.base import BaseCommand, CommandError
import datetime


class Command(BaseCommand):
    help = 'Get latest data'

    def handle(self, *args, **options):
        current = datetime.datetime.now()
        
        for endpoint in SensorEndpoint.objects.all():
            print("Now retrieving " + endpoint.name)
            get(endpoint, endpoint.timezone.localize(current))
