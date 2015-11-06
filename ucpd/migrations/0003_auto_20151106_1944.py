# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ucpd', '0002_auto_20151106_1917'),
    ]

    operations = [
        migrations.RenameField(
            model_name='statistics',
            old_name='avg_P',
            new_name='mean_P',
        ),
        migrations.RenameField(
            model_name='statistics',
            old_name='avg_Q',
            new_name='mean_Q',
        ),
        migrations.RenameField(
            model_name='statistics',
            old_name='avg_V',
            new_name='mean_V',
        ),
        migrations.RenameField(
            model_name='statistics',
            old_name='avg_count',
            new_name='mean_count',
        ),
    ]
