# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-12 23:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_atentionqueue_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='atentionqueue',
            name='attention_channels',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='atentionqueue',
            name='average_attention_time',
            field=models.PositiveIntegerField(default=600, editable=False),
        ),
    ]
