# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20150829_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finding',
            name='risk',
            field=models.CharField(max_length=50, verbose_name=b'Risk', choices=[(b'0', b'Informational'), (b'1', b'Low'), (b'2', b'Medium'), (b'3', b'High'), (b'4', b'Critical')]),
        ),
    ]
