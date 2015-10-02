# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20150924_2048'),
    ]

    operations = [
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
            ],
            options={
                'verbose_name': 'Url',
                'verbose_name_plural': 'Urls',
            },
        ),
        migrations.RemoveField(
            model_name='finding',
            name='url',
        ),
        migrations.AddField(
            model_name='url',
            name='finding',
            field=models.ForeignKey(blank=True, to='app.Finding', null=True),
        ),
    ]
