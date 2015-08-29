# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20150829_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='status',
            field=models.CharField(blank=True, max_length=50, verbose_name=b'Status', choices=[(b'progress', b'In Progress'), (b'retesting', b'Retesting'), (b'reporting', b'Reporting'), (b'postponed', b'Postponed'), (b'scheduled', b'Scheduled'), (b'completed', b'Completed')]),
        ),
        migrations.AlterField(
            model_name='finding',
            name='risk',
            field=models.CharField(max_length=50, verbose_name=b'Risk', choices=[(b'informational', b'Informational'), (b'low', b'Low'), (b'medium', b'Medium'), (b'high', b'High'), (b'critical', b'Critical')]),
        ),
    ]
