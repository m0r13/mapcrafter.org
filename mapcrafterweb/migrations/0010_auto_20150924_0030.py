# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapcrafterweb', '0009_auto_20150902_0044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='downloads',
        ),
        migrations.AddField(
            model_name='package',
            name='downloads_packages',
            field=models.IntegerField(default=0, verbose_name=b'downloads packages'),
        ),
        migrations.AddField(
            model_name='package',
            name='downloads_total',
            field=models.IntegerField(default=0, verbose_name=b'downloads total'),
        ),
    ]
