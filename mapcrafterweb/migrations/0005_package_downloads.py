# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapcrafterweb', '0004_auto_20140916_1847'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='downloads',
            field=models.IntegerField(default=0, verbose_name=b'downloads'),
            preserve_default=False,
        ),
    ]
