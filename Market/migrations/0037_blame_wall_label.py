# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-19 16:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0036_sell_comment_teacher_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='blame_wall',
            name='label',
            field=models.CharField(default='', max_length=20),
        ),
    ]
