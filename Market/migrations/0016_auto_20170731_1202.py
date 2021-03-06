# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-31 12:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0015_auto_20170731_1145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity_Wall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default='', max_length=100)),
                ('star', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Blame_Wall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default='', max_length=100)),
                ('star', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Confession_Wall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default='', max_length=100)),
                ('star', models.IntegerField(default=0)),
                ('Con_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MakeFriends_Wall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default='', max_length=100)),
                ('star', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher_Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=10)),
                ('email', models.CharField(default='', max_length=30)),
                ('phonenumber', models.CharField(default='', max_length=30)),
                ('Apartment', models.CharField(default='', max_length=20)),
                ('description', models.CharField(default='', max_length=100)),
                ('achievement', models.CharField(default='', max_length=100)),
                ('num_achievement', models.IntegerField(default=0)),
                ('star', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='location',
            name='app_location',
            field=models.CharField(default='', max_length=20),
        ),
    ]
