# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-22 02:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_auto_20161121_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atentionqueue',
            name='specialty',
            field=models.CharField(choices=[('1', 'pediatria'), ('2', 'sirugia')], max_length=1),
        ),
        migrations.DeleteModel(
            name='Specialty',
        ),
    ]
