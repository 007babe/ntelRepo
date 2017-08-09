from __future__ import unicode_literals  # Python 2.x 지원용

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible  # Python 2.x 지원용
class ComCd(models.Model):
    """ 공통코드 ModelClass
    """
    comCd = models.CharField(primary_key=True, db_column='com_cd', max_length=8, verbose_name='공통코드')
    grpCd = models.CharField(db_column='grp_cd', null=False, max_length=5, verbose_name='그룹코드')
    srtCd = models.CharField(db_column='srt_cd', max_length=3, null=True, blank=True, default=None, verbose_name='단축코드')
    comNm = models.CharField(db_column='com_nm', max_length=100, null=False, blank=False, default=None, verbose_name='코드명')
    comDesc = models.CharField(db_column='com_desc', max_length=200, null=True, blank=True, verbose_name='코드설명')
    ordSeq = models.IntegerField(db_column='ord_seq', default=1, verbose_name='순서')
    grpOpt = models.CharField(db_column='grp_opt', max_length=50, null=True, verbose_name='그룹옵션')
    grpOptDesc = models.CharField(db_column='grp_opt_desc', max_length=200, null=True, blank=True, verbose_name='옵션설명')
    cdCss = models.CharField(db_column='cd_css', max_length=200, null=True, blank=True, verbose_name='코드CSS')
    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    # 속성
    class Meta:
        db_table = "com_cd"
#        unique_together = (("grpCd", "comCd"),

    def publish(self):
        self.save()

    def __str__(self):
        return self.comCd


@python_2_unicode_compatible  # Python 2.x 지원용
class ComHttpStatus(models.Model):
    """ Http Code ModelClass
    """
    status = models.CharField(primary_key=True, db_column='status', max_length=3, verbose_name='Http 상태코드')
    title = models.CharField(db_column='title', max_length=100, verbose_name='타이틀')
    message = models.CharField(db_column='message', max_length=500, null=False, blank=False, default=None, verbose_name='메세지')
    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    # 속성
    class Meta:
        db_table = "com_http_status"

    def publish(self):
        self.save()

    def __str__(self):
        return self.comCd
