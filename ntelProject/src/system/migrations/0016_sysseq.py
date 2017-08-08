# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-01 19:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0015_auto_20170728_1710'),
    ]

    operations = [
        migrations.CreateModel(
            name='SysSeq',
            fields=[
                ('seqCd', models.CharField(db_column='seq_cd', max_length=6, primary_key=True, serialize=False, verbose_name='SEQ코드')),
                ('id', models.IntegerField(db_column='id', default=0, verbose_name='ID-순차번호')),
                ('seqDesc', models.TextField(blank=True, db_column='seqDesc', default=None, null=True, verbose_name='SEQ 설명')),
                ('useYn', models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')),
                ('regDt', models.DateTimeField(auto_now_add=True, db_column='reg_dt', null=True, verbose_name='등록일자')),
                ('modDt', models.DateTimeField(auto_now=True, db_column='mod_dt', verbose_name='수정일자')),
                ('modId', models.ForeignKey(blank=True, db_column='mod_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_system_sysseq_mod_id', to=settings.AUTH_USER_MODEL, verbose_name='수정자ID')),
                ('regId', models.ForeignKey(blank=True, db_column='reg_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_system_sysseq_reg_id', to=settings.AUTH_USER_MODEL, verbose_name='등록자ID')),
            ],
            options={
                'db_table': 'sys_seq',
            },
        ),
    ]