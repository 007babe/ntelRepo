# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-08 18:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0065_auto_20170908_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systelecom',
            name='telecomCd',
            field=models.CharField(db_column='telecom_cd', max_length=3, primary_key=True, serialize=False, verbose_name='통신사 코드'),
        ),
    ]