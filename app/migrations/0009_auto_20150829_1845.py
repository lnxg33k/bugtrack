# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20150829_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finding',
            name='risk',
            field=models.CharField(max_length=50, verbose_name=b'Risk', choices=[(b'1', b'Informational'), (b'2', b'Low'), (b'3', b'Medium'), (b'4', b'High'), (b'5', b'Critical')]),
        ),
    ]
