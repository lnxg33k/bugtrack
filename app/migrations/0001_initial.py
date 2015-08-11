# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'Assessment')),
                ('introduction', models.TextField(null=True, blank=True)),
                ('summary', models.TextField(null=True, blank=True)),
                ('is_published', models.BooleanField(default=False)),
                ('scope', models.TextField(null=True, blank=True)),
                ('methodology', models.TextField(null=True, blank=True)),
                ('caveats', models.TextField(null=True, blank=True)),
                ('created_at', models.DateField(null=True, verbose_name=b'Satrt Date', blank=True)),
                ('ends_at', models.DateField(null=True, verbose_name=b'End Date', blank=True)),
                ('status', models.CharField(blank=True, max_length=50, verbose_name=b'Status', choices=[(b'progress', b'In Progress'), (b'retesting', b'Retesting'), (b'reporting', b'Reporting'), (b'postponed', b'Postponed'), (b'scheduled', b'Scheduled'), (b'completed', b'Completed')])),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Assessment',
                'verbose_name_plural': 'Assessments',
            },
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(null=True, upload_to=b'images/%Y/%m/%d', blank=True)),
                ('title', models.CharField(max_length=50, null=True, verbose_name=b'Title', blank=True)),
            ],
            options={
                'verbose_name': 'POC',
                'verbose_name_plural': 'Proof Of Concept (Images)',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('is_replay', models.BooleanField(default=False, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.CreateModel(
            name='Finding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50, verbose_name=b'Finding')),
                ('risk', models.CharField(max_length=50, verbose_name=b'Risk', choices=[(b'informational', b'Informational'), (b'low', b'Low'), (b'medium', b'Medium'), (b'high', b'High'), (b'critical', b'Critical')])),
                ('is_fixed', models.BooleanField(default=False)),
                ('fix_date', models.DateTimeField(null=True, blank=True)),
                ('is_published', models.BooleanField(default=False)),
                ('allow_comments', models.BooleanField(default=True, verbose_name=b'Allow comments')),
                ('cvssv2', models.CharField(max_length=50, null=True, verbose_name=b'CVSSv2', blank=True)),
                ('overview', models.TextField(null=True, blank=True)),
                ('conditions', models.TextField(null=True, blank=True)),
                ('impact', models.TextField(null=True, blank=True)),
                ('recommendation', models.TextField(null=True, blank=True)),
                ('instance', models.TextField(null=True, verbose_name=b'Instances', blank=True)),
                ('url', models.TextField(null=True, verbose_name=b'Demonstration URLs', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assessment', models.ForeignKey(to='app.Assessment')),
            ],
            options={
                'verbose_name': 'Finding',
                'verbose_name_plural': 'Findings',
            },
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'Name')),
                ('url', models.CharField(max_length=250, verbose_name=b'URL')),
            ],
            options={
                'verbose_name': 'Reference',
                'verbose_name_plural': 'References',
            },
        ),
        migrations.CreateModel(
            name='Stakeholder',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='finding',
            name='fixed_by',
            field=models.ForeignKey(blank=True, to='app.Stakeholder', null=True),
        ),
        migrations.AddField(
            model_name='finding',
            name='references',
            field=models.ManyToManyField(to='app.Reference', blank=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='commenter',
            field=models.ForeignKey(to='app.Stakeholder'),
        ),
        migrations.AddField(
            model_name='comment',
            name='finding',
            field=models.ForeignKey(to='app.Finding'),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(related_name='replies', blank=True, to='app.Comment', null=True),
        ),
        migrations.AddField(
            model_name='attachment',
            name='finding',
            field=models.ForeignKey(blank=True, to='app.Finding', null=True),
        ),
        migrations.AddField(
            model_name='assessment',
            name='stakeholders',
            field=models.ManyToManyField(to='app.Stakeholder', blank=True),
        ),
    ]
