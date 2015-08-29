# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20150829_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finding',
            name='risk',
            field=models.CharField(max_length=50, verbose_name=b'Risk', choices=[(b'I', b'Informational'), (b'L', b'Low'), (b'M', b'Medium'), (b'H', b'High'), (b'C', b'Critical')]),
        ),
    ]
