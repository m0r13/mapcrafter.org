# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapcrafterweb', '0007_auto_20150812_1955'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='buildchannel',
            options={'verbose_name': 'build channel', 'verbose_name_plural': 'build channels'},
        ),
    ]
