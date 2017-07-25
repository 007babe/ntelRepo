# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-16 10:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20170715_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comcd',
            name='modId',
            field=models.ForeignKey(db_column='mod_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_com_cd_mod_id', to=settings.AUTH_USER_MODEL, verbose_name='수정자ID'),
        ),
    ]
