# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_assessment_publish_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='publish_date',
            field=models.DateField(null=True, verbose_name=b'Publish Date', blank=True),
        ),
    ]
