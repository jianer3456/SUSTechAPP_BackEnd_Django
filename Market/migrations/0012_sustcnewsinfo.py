# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-28 17:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0011_auto_20170707_2017'),
    ]

    operations = [
        migrations.CreateModel(
            name='SustcNewsInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=40)),
                ('newsImage', models.ImageField(blank=True, null=True, upload_to='./media/image/news/sustcimage')),
                ('newsUrl', models.CharField(default='', max_length=100)),
            ],
        ),
    ]
