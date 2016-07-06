# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-06 02:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_finding_fix_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created_at'], 'verbose_name': 'Comment', 'verbose_name_plural': 'Comments'},
        ),
        migrations.AlterField(
            model_name='finding',
            name='allow_comments',
            field=models.BooleanField(default=False, verbose_name=b'Allow comments'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='tags',
            field=models.ManyToManyField(to='app.Tag'),
        ),
    ]
