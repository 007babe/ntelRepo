from __future__ import unicode_literals  # Python 2.x 지원용

from django.db import models
from django.db.models.expressions import F
from django.db.models.query_utils import Q
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.
@python_2_unicode_compatible  # Python 2.x 지원용
class TelecomNetwork(models.Model):
    """
    통신망 ModelClass
    """
    networkId = models.CharField(db_column='network_id', primary_key=True, max_length=2, verbose_name='통신망 코드')
    networkNm = models.CharField(db_column='network_nm', max_length=100, null=True, blank=True, verbose_name='통신망 명')
    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    ordSeq = models.IntegerField(db_column='ord_seq', default=1, verbose_name='순서')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    class Meta:
        db_table = "telecom_network"

    def __str__(self):
        return self.networkId


@python_2_unicode_compatible  # Python 2.x 지원용
class TelecomCompany(models.Model):
    """
    통신사 ModelClass
    """
    companyId = models.CharField(db_column='company_id', primary_key=True, max_length=3, verbose_name='통신사 코드')
    companyNm = models.CharField(db_column='company_nm', max_length=100, null=True, blank=True, verbose_name='통신사 명')
    isMvno = models.BooleanField(db_column='is_mvno', null=False, blank=False, default=False, verbose_name='MVNO구분')
    ordSeq = models.IntegerField(db_column='ord_seq', default=1, verbose_name='순서')
    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    class Meta:
        db_table = "telecom_company"

    def __str__(self):
        return self.companyId


@python_2_unicode_compatible  # Python 2.x 지원용
class TelecomNetworkCompanyManager(models.Manager):
    '''
    망통신사 매니저
    '''
    def for_order(self, networkId=None, companyId=None, useYn=True):
        '''
        기본순서
        1. TelecomNetwork.ordSeq
        2. TelecomCompany.ordSeq
        '''
        qry = Q()

        qry &= Q(
            useYn__exact=useYn,
            networkId__useYn=useYn,
            companyId__useYn=useYn,
        )

        if networkId is not None:
            qry &= Q(
                networkId__exact=networkId
            )

        if companyId is not None:
            qry &= Q(
                companyId__exact=companyId
            )

        return self.get_queryset().filter(
            qry
        ).annotate(
            networkOrdSeq=F('networkId__ordSeq'),  # 통신망정렬순서
            companyOrdSeq=F('companyId__ordSeq'),  # 통신사정렬순서
        ).order_by(
            "networkOrdSeq",
            "companyOrdSeq",
        )


@python_2_unicode_compatible  # Python 2.x 지원용
class TelecomNetworkCompany(models.Model):
    """
    통신망 통신사 ModelClass
    """
    networkCompanyId = models.CharField(db_column='network_company_id', primary_key=True, max_length=6, verbose_name='통신망 통신사 코드')
    networkId = models.ForeignKey('telecom.TelecomNetwork', db_column='network_id', null=False, blank=False, default=None, related_name='r_%(app_label)s_%(class)s_network_id', verbose_name='통신망코드')
    companyId = models.ForeignKey('telecom.TelecomCompany', db_column='company_id', null=False, blank=False, default=None, related_name='r_%(app_label)s_%(class)s_company_id', verbose_name='통신사코드')
    networkCompanyNm = models.CharField(db_column='network_company_nm', max_length=100, null=True, blank=True, verbose_name='망통신사 명')
    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    # Manager
    objects = TelecomNetworkCompanyManager()

    class Meta:
        db_table = "telecom_network_company"

    def __str__(self):
        return self.networkCompanyId


class TelecomCallPlan(models.Model):
    """
    통신사별 요금제 ModelClass
    """
    networkCompanyId = models.ForeignKey('telecom.TelecomNetwork', db_column='network_company_id', null=False, blank=False, default=None, related_name='r_%(app_label)s_%(class)s_network_company_id', verbose_name='망별통신사코드')
    callPlanNm = models.CharField(db_column='call_plan_nm', max_length=100, null=True, blank=True, verbose_name='요금제 명')
    networkTp = models.ForeignKey('system.SysComCd', db_column='network_tp', related_name='r_%(app_label)s_%(class)s_service_tp', verbose_name='통신망구분')  # sys_com_cd.grp_cd = 'S0009'

    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    # Manager
#    objects = TelecomNetworkCompanyManager()

    class Meta:
        db_table = "telecom_call_plan"

    def __str__(self):
        return self.networkCompanyId
