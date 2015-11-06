# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ucpd', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_count', models.IntegerField(null=True)),
                ('max_V', models.IntegerField(null=True)),
                ('max_P', models.IntegerField(null=True)),
                ('max_Q', models.IntegerField(null=True)),
                ('min_count', models.IntegerField(null=True)),
                ('min_V', models.IntegerField(null=True)),
                ('min_P', models.IntegerField(null=True)),
                ('min_Q', models.IntegerField(null=True)),
                ('avg_count', models.IntegerField(null=True)),
                ('avg_V', models.IntegerField(null=True)),
                ('avg_P', models.IntegerField(null=True)),
                ('avg_Q', models.IntegerField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='bin',
            name='rank',
            field=models.IntegerField(null=True),
        ),
    ]
