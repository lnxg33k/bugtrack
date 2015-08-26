# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20150824_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='finding',
            name='is_fix_verified',
            field=models.BooleanField(default=False),
        ),
    ]
