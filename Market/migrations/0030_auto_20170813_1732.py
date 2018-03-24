# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-13 17:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0029_auto_20170811_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity_wall',
            name='endTime',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='activity_wall',
            name='limt_people',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='activity_wall',
            name='num_people',
            field=models.IntegerField(default=0),
        ),
    ]