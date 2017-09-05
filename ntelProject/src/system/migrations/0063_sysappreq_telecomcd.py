# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-04 20:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0062_remove_syscompanyaccount_telecomid'),
    ]

    operations = [
        migrations.AddField(
            model_name='sysappreq',
            name='telecomCd',
            field=models.CharField(blank=True, db_column='telecom_cd', default=None, max_length=100, null=True, verbose_name='통신사코드'),
        ),
    ]