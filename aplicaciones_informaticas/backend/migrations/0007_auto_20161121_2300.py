# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-21 23:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_auto_20161112_2325'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('triage_scale', models.CharField(choices=[('1', 'Atención inmediata (0 minutos de espera).'), ('2', 'Atención muy urgente (10 minutos de espera).'), ('3', 'Atención urgente (60 minutos de espera).'), ('4', 'Atención normal (120 minutos de espera).'), ('5', 'Atención no urgente (240 minutos de espera).')], max_length=1)),
                ('waittime', models.IntegerField()),
                ('start_time', models.DateTimeField()),
            ],
        ),
        migrations.AlterField(
            model_name='atentionqueue',
            name='health_center',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='queues', to='backend.HealthCenter'),
        ),
    ]