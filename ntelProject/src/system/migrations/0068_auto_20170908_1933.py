# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-08 19:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0067_auto_20170908_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='sysnetwork',
            name='ordSeq',
            field=models.IntegerField(db_column='ord_seq', default=1, verbose_name='순서'),
        ),
        migrations.AddField(
            model_name='systelecom',
            name='ordSeq',
            field=models.IntegerField(db_column='ord_seq', default=1, verbose_name='순서'),
        ),
    ]