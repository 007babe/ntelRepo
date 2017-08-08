# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-01 19:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0017_auto_20170801_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sysseq',
            name='seq',
            field=models.IntegerField(db_column='seq', default=0, verbose_name='순차번호'),
        ),
        migrations.AlterField(
            model_name='sysseq',
            name='seqDesc',
            field=models.CharField(blank=True, db_column='seq_desc', default=None, max_length=100, null=True, verbose_name='SEQ 설명'),
        ),
    ]