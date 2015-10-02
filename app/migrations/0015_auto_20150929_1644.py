# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20150929_1624'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instance', models.CharField(max_length=250, verbose_name=b'Instance')),
            ],
            options={
                'verbose_name': 'Instance',
                'verbose_name_plural': 'Affected Instances',
            },
        ),
        migrations.AlterModelOptions(
            name='url',
            options={'verbose_name': 'URL', 'verbose_name_plural': 'Affected URLs'},
        ),
        migrations.RemoveField(
            model_name='finding',
            name='instance',
        ),
        migrations.AddField(
            model_name='instance',
            name='finding',
            field=models.ForeignKey(blank=True, to='app.Finding', null=True),
        ),
    ]
