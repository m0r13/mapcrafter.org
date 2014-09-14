# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arch', models.CharField(max_length=255, verbose_name=b'architecture', choices=[(b'32', b'32 Bit'), (b'64', b'64 Bit')])),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date')),
                ('url', models.CharField(max_length=255, verbose_name=b'url')),
            ],
            options={
                'verbose_name': 'model',
                'verbose_name_plural': 'models',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PackageType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'name')),
                ('verbose_name', models.CharField(max_length=255, verbose_name=b'verbose name')),
            ],
            options={
                'verbose_name': 'package type',
                'verbose_name_plural': 'package types',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='package',
            name='type',
            field=models.ForeignKey(verbose_name=b'type', to='mapcrafterweb.PackageType'),
            preserve_default=True,
        ),
    ]
