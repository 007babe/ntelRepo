# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-09 15:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0043_auto_20170809_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sysappreq',
            name='reqStatus',
            field=models.ForeignKey(blank=True, db_column='req_status', default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_system_sysappreq_req_status', to='common.ComCd', verbose_name='요청진행상태'),
        ),
    ]
