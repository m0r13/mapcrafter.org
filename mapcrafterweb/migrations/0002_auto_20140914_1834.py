# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapcrafterweb', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='build',
            options={'verbose_name': 'build', 'verbose_name_plural': 'builds'},
        ),
        migrations.AlterModelOptions(
            name='platform',
            options={'verbose_name': 'platform', 'verbose_name_plural': 'platforms'},
        ),
        migrations.AddField(
            model_name='platform',
            name='download_dir',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'download directory'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='build',
            name='filename',
            field=models.CharField(max_length=255, verbose_name=b'filename'),
        ),
        migrations.AlterField(
            model_name='build',
            name='platform',
            field=models.ForeignKey(verbose_name=b'platform', to='mapcrafterweb.Platform'),
        ),
        migrations.AlterField(
            model_name='build',
            name='version',
            field=models.CharField(max_length=255, verbose_name=b'version'),
        ),
        migrations.AlterField(
            model_name='platform',
            name='name',
            field=models.CharField(max_length=255, verbose_name=b'name'),
        ),
    ]
