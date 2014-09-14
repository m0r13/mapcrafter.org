# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapcrafterweb', '0003_build_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='build',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'date'),
        ),
    ]
