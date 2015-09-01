# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapcrafterweb', '0008_auto_20150812_2259'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='buildchannel',
            options={'ordering': ['name'], 'verbose_name': 'build channel', 'verbose_name_plural': 'build channels'},
        ),
        migrations.AlterModelOptions(
            name='packagetype',
            options={'ordering': ['name'], 'verbose_name': 'package type', 'verbose_name_plural': 'package types'},
        ),
        migrations.AlterField(
            model_name='package',
            name='channel',
            field=models.ForeignKey(verbose_name=b'build channel', to='mapcrafterweb.BuildChannel'),
        ),
        migrations.AlterUniqueTogether(
            name='package',
            unique_together=set([('channel', 'type', 'arch', 'version_major', 'version_minor', 'version_build', 'version_commit', 'version_githash')]),
        ),
    ]
