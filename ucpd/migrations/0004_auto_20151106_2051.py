# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ucpd', '0003_auto_20151106_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistics',
            name='mean_10',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='statistics',
            name='mean_11',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='statistics',
            name='mean_12',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='statistics',
            name='mean_13',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='statistics',
            name='mean_14',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='mean_P',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='mean_Q',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='mean_V',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='mean_count',
            field=models.FloatField(null=True),
        ),
    ]
