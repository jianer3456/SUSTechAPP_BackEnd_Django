# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-04 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0020_user_pushid'),
    ]

    operations = [
        migrations.AddField(
            model_name='academicforuminfo',
            name='Detail_url',
            field=models.CharField(default='', max_length=50),
        ),
    ]