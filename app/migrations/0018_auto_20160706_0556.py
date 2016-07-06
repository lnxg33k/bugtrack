# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20160706_0541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='tags',
            field=models.ManyToManyField(to='app.Tag', blank=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.CharField(unique=True, max_length=200),
        ),
    ]
