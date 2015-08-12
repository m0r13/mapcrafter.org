# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapcrafterweb', '0006_package_visible'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildChannel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'name')),
                ('verbose_name', models.CharField(max_length=255, verbose_name=b'verbose name')),
            ],
            options={
                'verbose_name': 'build channels',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='package',
            options={'ordering': ['-version_major', '-version_minor', '-version_build', '-version_commit', '-type', '-arch', '-channel'], 'verbose_name': 'package', 'verbose_name_plural': 'packages'},
        ),
        migrations.AddField(
            model_name='package',
            name='channel',
            field=models.ForeignKey(default=None, verbose_name=b'build channel', to='mapcrafterweb.BuildChannel', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='package',
            name='version_githash',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'version githash'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='package',
            name='downloads',
            field=models.IntegerField(default=0, verbose_name=b'downloads'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='package',
            name='version_build',
            field=models.IntegerField(default=0, verbose_name=b'version build'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='package',
            name='version_commit',
            field=models.IntegerField(default=0, verbose_name=b'version commit'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='package',
            unique_together=set([('type', 'arch', 'version_major', 'version_minor', 'version_build', 'version_commit', 'version_githash')]),
        ),
    ]
