# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orm', '0005_auto_20160118_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='customimagepackage',
            name='project',
            field=models.ForeignKey(to='orm.Project', null=True),
        ),
    ]
