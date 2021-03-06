# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-17 14:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0005_remove_sysmenu_menucompanytp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='syscompany',
            name='companyGrade',
            field=models.ForeignKey(blank=True, db_column='company_grade', default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_system_syscompany_company_grade', to='common.ComCd', verbose_name='회사등급'),
        ),
        migrations.AlterField(
            model_name='syscompany',
            name='companyTp',
            field=models.ForeignKey(blank=True, db_column='company_tp', default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_system_syscompany_company_tp', to='common.ComCd', verbose_name='회사구분'),
        ),
        migrations.AlterField(
            model_name='syscompany',
            name='modId',
            field=models.ForeignKey(blank=True, db_column='mod_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_system_syscompany_mod_id', to=settings.AUTH_USER_MODEL, verbose_name='수정자ID'),
        ),
        migrations.AlterField(
            model_name='syscompany',
            name='regId',
            field=models.ForeignKey(blank=True, db_column='reg_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_system_syscompany_reg_id', to=settings.AUTH_USER_MODEL, verbose_name='등록자ID'),
        ),
        migrations.AlterField(
            model_name='sysmenu',
            name='modId',
            field=models.ForeignKey(blank=True, db_column='mod_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_system_sysmenu_mod_id', to=settings.AUTH_USER_MODEL, verbose_name='수정자ID'),
        ),
        migrations.AlterField(
            model_name='sysmenu',
            name='regId',
            field=models.ForeignKey(blank=True, db_column='reg_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_system_sysmenu_reg_id', to=settings.AUTH_USER_MODEL, verbose_name='등록자ID'),
        ),
        migrations.AlterField(
            model_name='sysmenu',
            name='upMenuId',
            field=models.ForeignKey(blank=True, db_column='up_menu_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_system_sysmenu_menu_id', to='system.SysMenu', verbose_name='상위메뉴ID'),
        ),
        migrations.AlterField(
            model_name='sysmenuauth',
            name='menuAuth',
            field=models.ForeignKey(db_column='menu_auth', on_delete=django.db.models.deletion.CASCADE, related_name='r_system_sysmenuauth_menu_auth', to='common.ComCd', verbose_name='메뉴권한'),
        ),
        migrations.AlterField(
            model_name='sysmenuauth',
            name='menuId',
            field=models.ForeignKey(db_column='menu_id', on_delete=django.db.models.deletion.CASCADE, related_name='r_system_sysmenuauth_menu_id', to='system.SysMenu', verbose_name='메뉴ID'),
        ),
        migrations.AlterField(
            model_name='sysmenuauth',
            name='modId',
            field=models.ForeignKey(blank=True, db_column='mod_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_system_sysmenuauth_mod_id', to=settings.AUTH_USER_MODEL, verbose_name='수정자ID'),
        ),
        migrations.AlterField(
            model_name='sysmenuauth',
            name='regId',
            field=models.ForeignKey(blank=True, db_column='reg_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_system_sysmenuauth_reg_id', to=settings.AUTH_USER_MODEL, verbose_name='등록자ID'),
        ),
        migrations.AlterField(
            model_name='sysmenucompanytp',
            name='companyTp',
            field=models.ForeignKey(db_column='company_tp', on_delete=django.db.models.deletion.CASCADE, related_name='r_system_sysmenucompanytp_company_tp', to='common.ComCd', verbose_name='메뉴회사타입'),
        ),
        migrations.AlterField(
            model_name='sysmenucompanytp',
            name='menuId',
            field=models.ForeignKey(db_column='menu_id', on_delete=django.db.models.deletion.CASCADE, related_name='r_system_sysmenucompanytp_menu_id', to='system.SysMenu', verbose_name='메뉴ID'),
        ),
        migrations.AlterField(
            model_name='sysmenucompanytp',
            name='modId',
            field=models.ForeignKey(blank=True, db_column='mod_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_system_sysmenucompanytp_mod_id', to=settings.AUTH_USER_MODEL, verbose_name='수정자ID'),
        ),
        migrations.AlterField(
            model_name='sysmenucompanytp',
            name='regId',
            field=models.ForeignKey(blank=True, db_column='reg_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_system_sysmenucompanytp_reg_id', to=settings.AUTH_USER_MODEL, verbose_name='등록자ID'),
        ),
        migrations.AlterField(
            model_name='sysshop',
            name='companyId',
            field=models.ForeignKey(blank=True, db_column='company_id', default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_system_sysshop_company_id', to='system.SysCompany'),
        ),
        migrations.AlterField(
            model_name='sysshop',
            name='modId',
            field=models.ForeignKey(blank=True, db_column='mod_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_system_sysshop_mod_id', to=settings.AUTH_USER_MODEL, verbose_name='수정자ID'),
        ),
        migrations.AlterField(
            model_name='sysshop',
            name='regId',
            field=models.ForeignKey(blank=True, db_column='reg_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_system_sysshop_reg_id', to=settings.AUTH_USER_MODEL, verbose_name='등록자ID'),
        ),
        migrations.AlterField(
            model_name='sysuser',
            name='modId',
            field=models.ForeignKey(blank=True, db_column='mod_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_system_sysuser_mod_id', to=settings.AUTH_USER_MODEL, verbose_name='수정자ID'),
        ),
        migrations.AlterField(
            model_name='sysuser',
            name='regId',
            field=models.ForeignKey(blank=True, db_column='reg_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_system_sysuser_reg_id', to=settings.AUTH_USER_MODEL, verbose_name='등록자ID'),
        ),
        migrations.AlterField(
            model_name='sysuser',
            name='shopId',
            field=models.ForeignKey(blank=True, db_column='shop_id', default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_system_sysuser_shop_id', to='system.SysShop', verbose_name='매장ID'),
        ),
        migrations.AlterField(
            model_name='sysuser',
            name='userAuth',
            field=models.ForeignKey(blank=True, db_column='user_auth', default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r_system_sysuser_user_auth', to='common.ComCd', verbose_name='사용자권한'),
        ),
    ]
