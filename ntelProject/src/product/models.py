from __future__ import unicode_literals  # Python 2.x 지원용

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible  # Python 2.x 지원용
class ProductMaker(models.Model):
    '''
    제품 제조사 정보
    '''
    makerCd = models.CharField(db_column='maker_cd', primary_key=True, max_length=10, blank=False, default=None, verbose_name='제조사코드')
    makerSrtCd = models.CharField(db_column='maker_srt_cd', max_length=3, null=False, blank=False, verbose_name='제조사단축코드')
    makerNm = models.CharField(db_column='maker_nm', max_length=100, null=False, blank=False, verbose_name='제조사명')
    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    class Meta:
        db_table = "product_maker"

    def __str__(self):
        return self.id


@python_2_unicode_compatible  # Python 2.x 지원용
class ProductPhone(models.Model):
    '''
    핸드폰 제품 정보
    '''
    makerCd = models.ForeignKey('product.ProductMaker', db_column='make_cd', null=False, blank=False, related_name='r_%(app_label)s_%(class)s_maker_cd', verbose_name='제조사코드')
    telecomCd = models.CharField(db_column='telecom_cd', max_length=100, null=False, blank=False, verbose_name='통신사코드')
    modelCd = models.CharField(db_column='model_cd', max_length=100, null=False, blank=False, verbose_name='제품모델코드')
    modelNm = models.CharField(db_column='model_nm', max_length=100, null=False, blank=False, verbose_name='제품모델명')
    phoneNm = models.CharField(db_column='phone_nm', max_length=100, null=False, blank=False, verbose_name='단말기명')
    netTp = models.CharField(db_column='net_tp', max_length=100, null=False, blank=False, verbose_name='단말기명')
    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    class Meta:
        db_table = "product_phone"

    def __str__(self):
        return self.id


# Create your models here.
@python_2_unicode_compatible  # Python 2.x 지원용
class ProductUsim(models.Model):
    '''
    Usim 제품 정보
    '''
    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    class Meta:
        db_table = "product_usim"

    def __str__(self):
        return self.id
