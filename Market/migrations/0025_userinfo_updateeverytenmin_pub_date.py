# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-07 15:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0024_auto_20170806_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo_updateeverytenmin',
            name='pub_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
