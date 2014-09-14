# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mapcrafterweb', '0004_auto_20140914_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='build',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date'),
        ),
    ]
