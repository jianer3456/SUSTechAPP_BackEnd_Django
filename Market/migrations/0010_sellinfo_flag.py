# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-07 12:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0009_auto_20170704_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellinfo',
            name='flag',
            field=models.IntegerField(default=0),
        ),
    ]
