# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapcrafterweb', '0005_package_downloads'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='visible',
            field=models.BooleanField(default=True, verbose_name=b'visible'),
            preserve_default=True,
        ),
    ]
