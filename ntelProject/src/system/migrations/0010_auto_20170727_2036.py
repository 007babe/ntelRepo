# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-27 20:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0009_sysmsg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sysuser',
            name='useYn',
            field=models.BooleanField(db_column='use_yn', default=False, verbose_name='사용여부'),
        ),
    ]