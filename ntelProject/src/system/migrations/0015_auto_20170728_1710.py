# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-28 17:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0014_auto_20170728_1709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sysappreq',
            name='companyCd',
        ),
        migrations.AddField(
            model_name='sysappreq',
            name='companyId',
            field=models.ForeignKey(blank=True, db_column='company_id', default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_system_sysappreq_company_cd', to='system.SysCompany', verbose_name='회사코드'),
        ),
    ]
