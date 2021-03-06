# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-27 19:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20170716_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comcd',
            name='modId',
            field=models.ForeignKey(blank=True, db_column='mod_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_common_comcd_mod_id', to=settings.AUTH_USER_MODEL, verbose_name='수정자ID'),
        ),
        migrations.AlterField(
            model_name='comcd',
            name='regId',
            field=models.ForeignKey(blank=True, db_column='reg_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_common_comcd_reg_id', to=settings.AUTH_USER_MODEL, verbose_name='등록자ID'),
        ),
    ]
