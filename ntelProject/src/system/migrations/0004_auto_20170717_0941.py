# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-17 09:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20170716_1048'),
        ('system', '0003_auto_20170716_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='sysmenu',
            name='menuCompanyTp',
            field=models.ForeignKey(blank=True, db_column='menu_company_tp', default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_sys_menu_menu_company_tp', to='common.ComCd', verbose_name='메뉴회사타입'),
        ),
        migrations.AlterField(
            model_name='sysmenu',
            name='upMenuId',
            field=models.ForeignKey(blank=True, db_column='up_menu_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_sys_menu_up_menu_id', related_query_name='rq_sys_menu_up_menu_id', to='system.SysMenu', verbose_name='상위메뉴ID'),
        ),
    ]