# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20150829_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='status',
            field=models.CharField(blank=True, max_length=50, verbose_name=b'Status', choices=[(b'progress', b'0'), (b'retesting', b'1'), (b'reporting', b'2'), (b'postponed', b'3'), (b'scheduled', b'4'), (b'completed', b'5')]),
        ),
        migrations.AlterField(
            model_name='finding',
            name='risk',
            field=models.CharField(max_length=50, verbose_name=b'Risk', choices=[(b'informational', b'0'), (b'low', b'1'), (b'medium', b'2'), (b'high', b'3'), (b'critical', b'4')]),
        ),
    ]
