# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_finding_is_fix_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='status',
            field=models.CharField(blank=True, max_length=50, verbose_name=b'Status', choices=[(b'0', b'In Progress'), (b'1', b'Retesting'), (b'2', b'Reporting'), (b'3', b'Postponed'), (b'4', b'Scheduled'), (b'5', b'Completed')]),
        ),
        migrations.AlterField(
            model_name='finding',
            name='risk',
            field=models.CharField(max_length=50, verbose_name=b'Risk', choices=[(b'0', b'Informational'), (b'1', b'Low'), (b'2', b'Medium'), (b'3', b'High'), (b'4', b'Critical')]),
        ),
    ]
