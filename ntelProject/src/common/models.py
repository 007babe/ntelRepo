from __future__ import unicode_literals  # Python 2.x 지원용

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible # Python 2.x 지원용
class TbComCd(models.Model):
    """ 공통코드 ModelClass
    """
    grpCd  = models.CharField(db_column='grp_cd', max_length=5) # 그룹코드
    comCd  = models.CharField(db_column='com_cd', max_length=10) # 공통코드
    comNm = models.CharField(db_column='com_nm', max_length=100) # 코드명
    ordSeq = models.IntegerField(db_column='ord_seq', default=1) # 순서
    useYn  = models.CharField(db_column='use_yn', max_length=1, default="Y") # 사용여부
    grpOpt = models.CharField(db_column='grp_opt', max_length=100, null=True) #그룹옵션
    regId  = models.CharField(db_column='reg_Id', max_length=10) # 등록자ID
    regDt  = models.DateTimeField(db_column='reg_dt', auto_now_add=True) # 등록일자
    modId  = models.CharField(db_column='mod_id', max_length=10) # 수정자ID
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True) # 수정일자
    
    # 속성
    class Meta:
        db_table="tb_com_cd"
        unique_together = (("grpCd", "comCd"),)
    
    def publish(self):
        self.save()
        
    def __str__(self):
        return models.Model.__str__(self)
    
class UserProfile(models.Model):
    """
    장고 User모델 OnToOne 모델 생성
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    zip_cd = models.CharField(db_column='zip_cd', max_length=6, blank=True)    
    addr = models.TextField(db_column='addr', max_length=500, blank=True)
    
    class Meta:
        db_table = "tb_user_profile"
        
    
    
