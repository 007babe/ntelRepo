from __future__ import unicode_literals  # Python 2.x 지원용

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible  # Python 2.x 지원용
class ProductMaker(models.Model):
    '''
    제품 제조사 정보
    '''
    makerId = models.CharField(db_column='maker_id', primary_key=True, max_length=10, blank=False, default=None, verbose_name='제조사ID')
    makerNm = models.CharField(db_column='maker_nm', max_length=100, null=False, blank=False, verbose_name='제조사명')
    srtCd = models.CharField(db_column='srt_cd', max_length=3, null=False, blank=False, verbose_name='제조사단축코드')
    ordSeq = models.IntegerField(db_column='ord_seq', default=1, verbose_name='순서')
    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    class Meta:
        db_table = "product_maker"

    def __str__(self):
        return self.makerId


@python_2_unicode_compatible  # Python 2.x 지원용
class ProductColor(models.Model):

    colorId = models.CharField(db_column='color_id', primary_key=True, max_length=10, blank=False, default=None, verbose_name='핸드폰제품ID')
    colorNm = models.CharField(db_column='color_nm', max_length=100, null=False, blank=False, verbose_name='색깔명')
    colorRgb = models.CharField(db_column='color_rgb', max_length=7, null=False, blank=False, verbose_name='색깔RGB코드')
    colorImg = models.CharField(db_column='color_img', max_length=256, null=False, blank=False, verbose_name='색깔이미지파일')
    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    class Meta:
        db_table = "product_color"

    def __str__(self):
        return self.id


@python_2_unicode_compatible  # Python 2.x 지원용
class ProductModelColor(models.Model):

    modelId = models.ForeignKey('product.ProductModel', db_column='model_id', null=False, blank=False, related_name='r_%(app_label)s_%(class)s_product_id', verbose_name='제품코드')
    colorId = models.ForeignKey('product.ProductColor', db_column='color_id', null=False, blank=False, related_name='r_%(app_label)s_%(class)s_color_id', verbose_name='색깔코드')
    modelImg = models.CharField(db_column='product_img', max_length=256, null=False, blank=False, verbose_name='색깔적용모델이미지파일')

    # 단종여부
    closedYn = models.BooleanField(db_column='closed_yn', null=False, blank=False, default=False, verbose_name='단종여부')
    closedDt = models.DateTimeField(db_column='closed_dt', null=True, blank=True, verbose_name='등록일자')
    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    class Meta:
        db_table = "product_model_color"

    def __str__(self):
        return self.id


@python_2_unicode_compatible  # Python 2.x 지원용
class ProductModel(models.Model):
    '''
    휴대폰 모델 정보
    '''
    modelId = models.CharField(db_column='model_id', primary_key=True, max_length=12, blank=False, default=None, verbose_name='모델ID')
    makerId = models.ForeignKey('product.ProductMaker', db_column='maker_id', null=False, blank=False, related_name='r_%(app_label)s_%(class)s_maker_id', verbose_name='제조사코드')
    modelNm = models.CharField(db_column='model_nm', max_length=100, null=False, blank=False, default=None, verbose_name='모델명')
    modelCd = models.CharField(db_column='model_cd', max_length=100, null=False, blank=False, default=None, verbose_name='모델코드')
    modelTp = models.ForeignKey('system.SysComCd', db_column='model_tp', null=True, blank=False, default=None, related_name='r_%(app_label)s_%(class)s_model_tp', verbose_name='모델종류') # ComCd.grpCd = 'G0001'

    # 모델 SPEC
    releaseDt = models.DateTimeField(db_column='release_dt', null=True, blank=True, verbose_name='출시일자')
    factoryPrice = models.IntegerField(db_column='factory_price', null=False, blank=False, default=0, verbose_name='출고가격')
    specOs = models.TextField(db_column='spec_os', null=True, blank=True, verbose_name='제품스펙-OS')
    specCpu = models.TextField(db_column='spec_cpu', null=True, blank=True, verbose_name='제품스펙-CPU')
    specDisp = models.TextField(db_column='spec_disp', null=True, blank=True, verbose_name='제품스펙-디스플레이')
    specScreen = models.TextField(db_column='spec_screen', null=True, blank=True, verbose_name='제품스펙-화면크기')
    specCamera = models.TextField(db_column='spec_camera', null=True, blank=True, verbose_name='제품스펙-카메라')
    specRam = models.TextField(db_column='spec_ram', null=True, blank=True, verbose_name='제품스펙-RAM')
    specMemoryIn = models.TextField(db_column='spec_memory_in', null=True, blank=True, verbose_name='제품스펙-내장메모리')
    specMemoryExt = models.TextField(db_column='spec_memory_ext', null=True, blank=True, verbose_name='제품스펙-외장메모리')
    specBattery = models.TextField(db_column='spec_battery', null=True, blank=True, verbose_name='제품스펙-배터리')
    specDesc = models.TextField(db_column='spec_desc', null=True, blank=True, verbose_name='제품스펙-전체설명')
    specComponent = models.TextField(db_column='spec_component', null=True, blank=True, verbose_name='제품스펙-구성품')
    specNfcYn = models.BooleanField(db_column='spec_nfc_yn', null=False, blank=False, default=False, verbose_name='NFC가능여부')
    specDmbYn = models.BooleanField(db_column='spec_dmb_yn', null=False, blank=False, default=False, verbose_name='DMB가능여부')
    usimTp = models.ForeignKey('system.SysComCd', db_column='usim_tp', null=True, blank=False, default=None, related_name='r_%(app_label)s_%(class)s_usim_tp', verbose_name='사용가능USIM종류') # ComCd.grpCd = 'G0025'

    # 단종여부
    closedYn = models.BooleanField(db_column='closed_yn', null=False, blank=False, default=False, verbose_name='단종여부')
    closedDt = models.DateTimeField(db_column='closed_dt', null=True, blank=True, verbose_name='등록일자')

    ordSeq = models.IntegerField(db_column='ord_seq', default=1, verbose_name='순서')

    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    class Meta:
        db_table = "product_model"

    def __str__(self):
        return self.modelId


@python_2_unicode_compatible  # Python 2.x 지원용
class ProductPhone(models.Model):
    '''
    휴대폰 제품 정보
    '''
    productId = models.CharField(db_column='product_id', primary_key=True, max_length=10, blank=False, default=None, verbose_name='제품ID')
    makerId = models.ForeignKey('product.ProductMaker', db_column='make_id', null=False, blank=False, related_name='r_%(app_label)s_%(class)s_maker_id', verbose_name='제조사코드')
    networkCompanyId = models.ForeignKey('telecom.TelecomNetworkCompany', db_column='network_company_id', null=False, blank=False, default=None, related_name='r_%(app_label)s_%(class)s_network_company_id', verbose_name='통신망코드')
    productNm = models.CharField(db_column='product_nm', max_length=100, null=False, blank=False, default=None, verbose_name='제품명')

    modelCd = models.CharField(db_column='model_cd', max_length=100, null=False, blank=False, default=None, verbose_name='제품모델코드')
    productCd = models.CharField(db_column='product_cd', max_length=100, null=False, blank=False, default=None, verbose_name='제품코드')
    productTp = models.ForeignKey('system.SysComCd', db_column='product_tp', null=True, blank=False, default=None, related_name='r_%(app_label)s_%(class)s_product_tp', verbose_name='제품종류') # ComCd.grpCd = 'G0001'

    # 제품 SPEC
    releaseDt = models.DateTimeField(db_column='releaseDt', null=True, blank=True, verbose_name='출시일자')
    factoryPrice = models.IntegerField(db_column='factory_price', null=False, blank=False, default=0, verbose_name='출고가격')
    specOs = models.TextField(db_column='spec_os', null=True, blank=True, verbose_name='제품스펙-OS')
    specCpu = models.TextField(db_column='spec_cpu', null=True, blank=True, verbose_name='제품스펙-CPU')
    specDisp = models.TextField(db_column='spec_display', null=True, blank=True, verbose_name='제품스펙-디스플레이')
    specScreen = models.TextField(db_column='spec_screen', null=True, blank=True, verbose_name='제품스펙-화면크기')
    specCamera = models.TextField(db_column='spec_camera', null=True, blank=True, verbose_name='제품스펙-카메라')
    specRam = models.TextField(db_column='spec_ram', null=True, blank=True, verbose_name='제품스펙-RAM')
    specMemoryIn = models.TextField(db_column='spec_memory_in', null=True, blank=True, verbose_name='제품스펙-내장메모리')
    specMemoryExt = models.TextField(db_column='spec_memory_ext', null=True, blank=True, verbose_name='제품스펙-외장메모리')
    specBattery = models.TextField(db_column='spec_battery', null=True, blank=True, verbose_name='제품스펙-배터리')
    specDesc = models.TextField(db_column='spec_desc', null=True, blank=True, verbose_name='제품스펙-전체설명')
    specComponent = models.TextField(db_column='spec_component', null=True, blank=True, verbose_name='제품스펙-전체설명')
    specNfcYn = models.BooleanField(db_column='spec_nfc_yn', null=False, blank=False, default=False, verbose_name='NFC가능여부')
    specDmbYn = models.BooleanField(db_column='spec_dmb_yn', null=False, blank=False, default=False, verbose_name='DBM가능여부')
    usimTp = models.ForeignKey('system.SysComCd', db_column='usim_tp', null=True, blank=False, default=None, related_name='r_%(app_label)s_%(class)s_usim_tp', verbose_name='사용가능USIM종류') # ComCd.grpCd = 'G0025'

    # 단종여부
    closedYn = models.BooleanField(db_column='closed_yn', null=False, blank=False, default=False, verbose_name='단종여부')
    closedDt = models.DateTimeField(db_column='closed_dt', null=True, blank=True, verbose_name='등록일자')

    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    class Meta:
        db_table = "product_phone"

    def __str__(self):
        return self.productId


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
