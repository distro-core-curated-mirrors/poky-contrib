# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orm', '0012_use_release_instead_of_up_branch'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='local_source_dir',
            field=models.TextField(null=True, default=None),
        ),
    ]
