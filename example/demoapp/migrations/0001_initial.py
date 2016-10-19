# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import unitology.fields
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('units', models.CharField(default=b'imperial', help_text='User specific system of measurements...', max_length=12, choices=[(b'imperial', 'Standard (lbs/ft/in)'), (b'metric', 'Metric (kg/cm)')])),
                ('name', models.CharField(max_length=128)),
                ('weight', unitology.fields.WeightField(default=Decimal('0.00'), null=True, max_digits=10, decimal_places=2, blank=True)),
                ('height', unitology.fields.HeightField(default=Decimal('0.00'), null=True, max_digits=10, decimal_places=2, blank=True)),
            ],
        ),
    ]
