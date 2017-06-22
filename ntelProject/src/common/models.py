from __future__ import unicode_literals # Python 2.x 지원용
from django.utils.encoding import python_2_unicode_compatible

from django.db import models

# Create your models here.

@python_2_unicode_compatible # Python 2.x 지원용
class TbComCd(models.Model):
    """ 공통코드 ModelClass
    """
    grpCd  = models.CharField(verbose_name='grp_cd', max_length=5) # 그룹코드
    comCd  = models.CharField(max_length=10) # 공통코드
    comNm = models.CharField(max_length=100) # 코드명
    ordSeq = models.IntegerField(default=1) # 순서
    useYn  = models.CharField(max_length=1, default="Y") # 사용여부
    grpOpt = models.CharField(max_length=100, null=True) #그룹옵션
    regId  = models.CharField(max_length=10) # 등록자ID
    regDt  = models.DateTimeField(auto_now_add=True) # 등록일자
    modId  = models.CharField(max_length=10) # 수정자ID
    modDt = models.DateTimeField(auto_now=True) # 수정일자
    
    # 속성
    class Meta:
        db_table="TB_COM_CD"
        unique_together = (("grpCd", "comCd"),)
    
    def publish(self):
        self.save()
        
    def __str__(self):
        return models.Model.__str__(self)
