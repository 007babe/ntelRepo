# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-31 15:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_comhttpstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comhttpstatus',
            name='status',
            field=models.CharField(db_column='status', max_length=3, primary_key=True, serialize=False, verbose_name='Http 상태코드'),
        ),
    ]
