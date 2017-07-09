from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from intake.models import SensorSite, SensorEndpoint, Generated
import datetime

def site_list(request):
    template = 'intake/site-list.html'
    sites = SensorSite.objects.all()
    last_day = Generated.objects.filter(timestamp__gte=Generated.objects.all().latest('timestamp').timestamp - datetime.timedelta(days=1)).aggregate(Sum('value'))
    last_month = Generated.objects.filter(timestamp__gte=Generated.objects.all().latest('timestamp').timestamp - datetime.timedelta(days=30)).aggregate(Sum('value'))
    last_year = Generated.objects.filter(timestamp__gte=Generated.objects.all().latest('timestamp').timestamp - datetime.timedelta(days=365)).aggregate(Sum('value'))
    context = {
        'title': 'Site',
        'sites': sites,
        'site_count': SensorSite.objects.count(),
        'sensor_count': SensorEndpoint.objects.count(),
        'last_day': last_day['value__sum'],
        'last_month': last_month['value__sum'],
        'last_year': last_year['value__sum'],
    } 

    return render(request, template, context)

def login_form(request):
    template = 'intake/login.html'
    context = {
        'title': 'Login',
    } 

    return render(request, template, context)

def auth(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        return login_form(request)

@login_required
def site_detail(request, site_id):
    template = 'intake/site-detail.html'
    site = SensorSite.objects.get(id=site_id)
    sensors = SensorEndpoint.objects.filter(site=site)
    context = {
        'title': site.name + " sensors",
        'sensors': sensors
    }

    return render(request, template, context)

@login_required
def sensor_detail(request, sensor_id):
    template = 'intake/sensor-detail.html'
    sensor = SensorEndpoint.objects.get(id=sensor_id)
    context = {
        'title': sensor.name,
        'sensor': sensor
    }
    
    return render(request, template, context)
