from __future__ import unicode_literals  # Python 2.x 지원용

from django.db import models
from django.db.models.expressions import F
from django.db.models.query_utils import Q
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.
@python_2_unicode_compatible  # Python 2.x 지원용
class SysNetwork(models.Model):
    """
    통신망 ModelClass
    """
    networkCd = models.CharField(db_column='network_cd', primary_key=True, max_length=2, verbose_name='통신망 코드')
    networkNm = models.CharField(db_column='network_nm', max_length=100, null=True, blank=True, verbose_name='통신망 명')
    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    ordSeq = models.IntegerField(db_column='ord_seq', default=1, verbose_name='순서')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    class Meta:
        db_table = "sys_network"

    def __str__(self):
        return self.networkCd


@python_2_unicode_compatible  # Python 2.x 지원용
class SysTelecom(models.Model):
    """
    통신사 ModelClass
    """
    telecomCd = models.CharField(db_column='telecom_cd', primary_key=True, max_length=3, verbose_name='통신사 코드')
    telecomNm = models.CharField(db_column='telecom_nm', max_length=100, null=True, blank=True, verbose_name='통신사 명')
    isMvno = models.BooleanField(db_column='is_mvno', null=False, blank=False, default=False, verbose_name='MVNO구분')
    ordSeq = models.IntegerField(db_column='ord_seq', default=1, verbose_name='순서')
    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    class Meta:
        db_table = "sys_telecom"

    def __str__(self):
        return self.telecomCd


@python_2_unicode_compatible  # Python 2.x 지원용
class SysNetworkTelecomManager(models.Manager):
    '''
    망통신사 매니저
    '''
    def for_order(self, networkCd=None, telecomCd=None, useYn=True):
        '''
        기본순서
        1. SysNetwork.ordSeq
        2. SysTelecom.ordSeq
        '''
        qry = Q()

        qry &= Q(
            useYn__exact=useYn,
            networkCd__useYn=useYn,
            telecomCd__useYn=useYn,
        )

        if networkCd is not None:
            qry &= Q(
                networkCd__exact=networkCd
            )

        if telecomCd is not None:
            qry &= Q(
                telecomCd__exact=telecomCd
            )

        return self.get_queryset().filter(
            qry
        ).annotate(
            networkOrdSeq=F('networkCd__ordSeq'),  # 통신망정렬순서
            telecomOrdSeq=F('telecomCd__ordSeq'),  # 통신사정렬순서
        ).order_by(
            "networkOrdSeq",
            "telecomOrdSeq",
        )


@python_2_unicode_compatible  # Python 2.x 지원용


class SysNetworkTelecom(models.Model):
    """
    통신망 통신사 ModelClass
    """
    networkTelecomCd = models.CharField(db_column='network_telecom_cd', primary_key=True, max_length=6, verbose_name='통신망 통신사 코드')
    networkCd = models.ForeignKey('system.SysNetwork', db_column='network_cd', null=False, blank=False, related_name='r_%(app_label)s_%(class)s_network_cd', verbose_name='통신망코드')
    telecomCd = models.ForeignKey('system.SysTelecom', db_column='telecom_cd', null=False, blank=False, related_name='r_%(app_label)s_%(class)s_telecom_cd', verbose_name='통신사코드')
    networkTelecomNm = models.CharField(db_column='network_telecom_nm', max_length=100, null=True, blank=True, verbose_name='망통신사 명')
    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    # Manager
    objects = SysNetworkTelecomManager()

    class Meta:
        db_table = "sys_network_telecom"

    def __str__(self):
        return self.networkTelecomCd
