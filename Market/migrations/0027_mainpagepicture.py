# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-10 10:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0026_userbooksinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainPagePicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(default='', max_length=20)),
                ('fSmallImg', models.CharField(default='', max_length=200)),
                ('fBigImg', models.CharField(default='', max_length=200)),
                ('pub_change_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
