# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-19 12:24
from __future__ import unicode_literals

from django.db import migrations
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('intake', '0005_auto_20170619_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensorsite',
            name='timezone',
            field=timezone_field.fields.TimeZoneField(default='US/Hawaii'),
        ),
    ]