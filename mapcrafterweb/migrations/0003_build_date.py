# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('mapcrafterweb', '0002_auto_20140914_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='build',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name=b'date'),
            preserve_default=True,
        ),
    ]
