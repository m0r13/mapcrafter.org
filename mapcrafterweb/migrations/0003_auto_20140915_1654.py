# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapcrafterweb', '0002_auto_20140914_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='version_build',
            field=models.IntegerField(default=0, verbose_name=b'version build'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='package',
            name='version_commit',
            field=models.IntegerField(default=0, verbose_name=b'version commit'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='package',
            name='version_major',
            field=models.IntegerField(default=0, verbose_name=b'version major'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='package',
            name='version_minor',
            field=models.IntegerField(default=0, verbose_name=b'version minor'),
            preserve_default=False,
        ),
    ]
