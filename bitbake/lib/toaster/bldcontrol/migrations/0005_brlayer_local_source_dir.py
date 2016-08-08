# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bldcontrol', '0004_auto_20160523_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='brlayer',
            name='local_source_dir',
            field=models.CharField(max_length=254, null=True),
        ),
    ]
