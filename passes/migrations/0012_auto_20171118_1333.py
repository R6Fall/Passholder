# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-18 13:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0011_auto_20171118_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crypto',
            name='pub_date',
            field=models.DateTimeField(default='2017-11-18 13:33:04.440387+00:00', verbose_name='date created'),
        ),
    ]
