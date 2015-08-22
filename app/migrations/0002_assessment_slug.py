# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='slug',
            field=models.SlugField(unique=True, null=True, blank=True),
        ),
    ]
