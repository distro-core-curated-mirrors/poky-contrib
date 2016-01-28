# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orm', '0005_task_field_separation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='build',
            name='build_name',
        ),
    ]
