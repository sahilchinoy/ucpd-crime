# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(srid=4326, null=True)),
                ('population', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caseno', models.CharField(help_text=b'Case number', max_length=10, db_index=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('date', models.DateField(null=True, blank=True)),
                ('time', models.TimeField(null=True, blank=True)),
                ('offense', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('category', models.CharField(default=b'N', max_length=1, choices=[(b'V', b'Violent'), (b'P', b'Property'), (b'Q', b'Quality of life'), (b'N', b'Uncategorized')])),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True)),
                ('hbin', models.ForeignKey(related_name='incidents', to='ucpd.Bin', null=True)),
            ],
            options={
                'ordering': ['-caseno'],
            },
        ),
    ]
