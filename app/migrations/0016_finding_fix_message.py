# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20150929_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='finding',
            name='fix_message',
            field=models.TextField(null=True, blank=True),
        ),
    ]
