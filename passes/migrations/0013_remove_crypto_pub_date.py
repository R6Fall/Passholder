# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-18 13:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0012_auto_20171118_1333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crypto',
            name='pub_date',
        ),
    ]
