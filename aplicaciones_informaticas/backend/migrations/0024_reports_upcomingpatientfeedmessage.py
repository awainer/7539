# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-09 15:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0023_atentionqueue_max_capacity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='UpcomingPatientFeedMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eta', models.DateTimeField()),
                ('health_center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.HealthCenter')),
                ('queue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.AtentionQueue')),
                ('triageScale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.TriageScaleLevel')),
            ],
        ),
    ]
