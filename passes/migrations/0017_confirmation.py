# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-04 16:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0016_auto_20171210_1242'),
    ]

    operations = [
        migrations.CreateModel(
            name='Confirmation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.IntegerField(default=111111)),
                ('user_id', models.IntegerField(default=1)),
            ],
        ),
    ]