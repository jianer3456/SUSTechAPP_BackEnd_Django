# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-25 02:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0002_auto_20170625_0141'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='scope',
            new_name='score',
        ),
    ]
