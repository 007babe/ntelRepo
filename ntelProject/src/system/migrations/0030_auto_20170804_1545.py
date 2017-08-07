# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-04 15:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0029_auto_20170803_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sysappreq',
            name='telNo1',
            field=models.CharField(db_column='tel_no1', default=None, max_length=5, verbose_name='회사전화1'),
        ),
        migrations.AlterField(
            model_name='sysappreq',
            name='telNo2',
            field=models.CharField(db_column='tel_no2', default=None, max_length=5, verbose_name='회사전화2'),
        ),
        migrations.AlterField(
            model_name='sysappreq',
            name='telNo3',
            field=models.CharField(db_column='tel_no3', default=None, max_length=5, verbose_name='회사전화3'),
        ),
        migrations.AlterField(
            model_name='sysappreq',
            name='userId',
            field=models.CharField(db_column='user_id', max_length=20, verbose_name='대표사용자아이디'),
        ),
    ]
