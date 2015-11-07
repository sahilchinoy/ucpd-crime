# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ucpd', '0004_auto_20151106_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistics',
            name='bin_count',
            field=models.IntegerField(null=True),
        ),
    ]
