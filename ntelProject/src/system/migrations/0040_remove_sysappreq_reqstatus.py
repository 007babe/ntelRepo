# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-09 14:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0039_auto_20170809_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sysappreq',
            name='reqStatus',
        ),
    ]