# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-01 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0016_auto_20170731_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='realname',
            field=models.CharField(default='', max_length=20),
        ),
    ]