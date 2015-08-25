# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_assessment_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='publish_date',
            field=models.DateField(default=datetime.datetime.now, verbose_name=b'Publish Date', blank=True),
        ),
    ]
