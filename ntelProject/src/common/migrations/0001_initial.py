# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-15 22:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ComCd',
            fields=[
                ('comCd', models.CharField(db_column='com_cd', max_length=8, primary_key=True, serialize=False, verbose_name='공통코드')),
                ('grpCd', models.CharField(db_column='grp_cd', max_length=5, verbose_name='그룹코드')),
                ('comNm', models.CharField(db_column='com_nm', default=None, max_length=100, verbose_name='코드명')),
                ('comDesc', models.CharField(blank=True, db_column='com_desc', max_length=200, null=True, verbose_name='코드설명')),
                ('ordSeq', models.IntegerField(db_column='ord_seq', default=1, verbose_name='순서')),
                ('grpOpt', models.CharField(db_column='grp_opt', max_length=50, null=True, verbose_name='그룹옵션')),
                ('grpOptDesc', models.CharField(blank=True, db_column='grp_opt_desc', max_length=200, null=True, verbose_name='옵션설명')),
                ('useYn', models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')),
                ('regDt', models.DateTimeField(auto_now_add=True, db_column='reg_dt', null=True, verbose_name='등록일자')),
                ('modDt', models.DateTimeField(auto_now=True, db_column='mod_dt', verbose_name='수정일자')),
            ],
            options={
                'db_table': 'com_cd',
            },
        ),
    ]
