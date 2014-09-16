# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapcrafterweb', '0003_auto_20140915_1654'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='package',
            options={'ordering': ['-version_major', '-version_minor', '-version_build', '-version_commit', '-type', '-arch'], 'verbose_name': 'package', 'verbose_name_plural': 'packages'},
        ),
    ]
