# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-21 19:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion

from common.model.fields import ThumbnailImageField


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SampleAlbum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', max_length=50, verbose_name='앨범명')),
                ('description', models.CharField(blank=True, db_column='description', max_length=100, verbose_name='album description')),
            ],
            options={
                'db_table': 'sample_album',
            },
        ),
        migrations.CreateModel(
            name='SamplePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_column='title', max_length=50, verbose_name='사진제목')),
                ('image', ThumbnailImageField(upload_to='photo/%Y/%m')),
                ('description', models.CharField(blank=True, db_column='description', max_length=100, verbose_name='photo description')),
                ('upload_date', models.DateTimeField(auto_now_add=True, db_column='upload_date', verbose_name='업로드일자')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sample.SampleAlbum')),
            ],
            options={
                'db_table': 'sample_photo',
            },
        ),
    ]
