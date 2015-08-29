# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20150829_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finding',
            name='risk',
            field=models.CharField(max_length=50, verbose_name=b'Risk', choices=[(0, b'Informational'), (1, b'Low'), (2, b'Medium'), (3, b'High'), (4, b'Critical')]),
        ),
    ]
