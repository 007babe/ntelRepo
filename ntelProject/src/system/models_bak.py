from __future__ import unicode_literals  # Python 2.x 지원용

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

class Company(models.Model):
    """엔텔 사용 회사 정보
    """
    company_cd = models.CharField(db_column='company_cd', max_length=100, blank=True)
    company_nm = models.CharField(db_column='company_nm', max_length=100, blank=True)
    company_tp = models.CharField(db_column='company_tp', max_length=100, blank=True)
    tel_no = models.CharField(db_column='tel_no', max_length=10, blank=True) # 전화번호(대표)
    cell_no = models.CharField(db_column='cell_no', max_length=10, blank=True) # 휴대폰번호(대표)
    zip_cd = models.CharField(db_column='zip_cd', max_length=6, blank=True) # 우편번호(회사)   
    addr1 = models.TextField(db_column='addr_1', max_length=200, blank=True) # 우편번호 기본 주소(회사)
    addr2 = models.TextField(db_column='addr_2', max_length=200, blank=True) # 상세주소(회사)
    reg_id  = models.CharField(db_column='reg_id', max_length=10, null=False, default='system') # 등록자ID
    reg_dt  = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True) # 등록일자
    mod_id  = models.CharField(db_column='mod_id', max_length=10, null=False, default='system') # 수정자ID
    mod_dt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True) # 수정일자

    class Meta:
        db_table = "sys_company"
        unique_together = (("company_cd",),)
        
    def __str__(self):
        return self.company_cd    
        
        
        
@python_2_unicode_compatible # Python 2.x 지원용
class SysUserManager(BaseUserManager):
    """
    시스템 사용자 관리 매니저
    """

    def create_user(self, email, cell_no, password=None):        
        """  
        일반 사용자 생성
        """
        if not email:
            raise ValueError('email은 필수 입력입니다.')

        if not cell_no:
            raise ValueError('휴대폰번호는 필수 입력입니다.')
        
        user = self.model(
            email = self.nomalize_email(email),
        )
        
        user.is_admin = False
        user.set_password(password)
        user.save(using = self._db)
        return User
    
    def create_superuser(self, email, cell_no, password):
        """
        Superuser 사용자 생성
        """
        user = self.create_user(
            email,
            password = password,
        )
        user.is_admin = True
        user.save(using = self._db)
        return user    

@python_2_unicode_compatible # Python 2.x 지원용
class SysUser(AbstractBaseUser):
    """장고 User모델 Customized
    """
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    
    # 추가 필드
    username_k = models.CharField(db_column='username_k', max_length=20, null=False, blank=False) # 사용자 이름(한국어)
    tel_no = models.CharField(db_column='tel_no', max_length=10, blank=True) # 전화번호
    cell_no = models.CharField(db_column='cell_no', max_length=20, blank=True) # 휴대폰번호
    zip_cd = models.CharField(db_column='zip_cd', max_length=6, blank=True) # 우편번호
    addr1 = models.TextField(db_column='addr1', max_length=200, blank=True) # 주소1
    addr2 = models.TextField(db_column='addr2', max_length=200, blank=True) # 주소2
    user_auth = models.CharField(db_column='user_auth', max_length=1, blank=True) # 사용자 권한(M: 시스템관리자, C: 대표, A:총괄, T:팀장, S:사원, I: 인턴)
    reg_id  = models.CharField(db_column='reg_id', max_length=10, null=False, default='system') # 등록자ID
    reg_dt  = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True) # 등록일자
    mod_id  = models.CharField(db_column='mod_id', max_length=10, null=False, default='system') # 수정자ID
    mod_dt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True) # 수정일자

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = SysUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['cell_no'] # 필수 입력 필드 정의
    
    def get_full_name(self):
        # The user is identified by their username
        return self.username

    def get_short_name(self):
        # The user is identified by their username
        return self.username

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        #"Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        #"Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        #"Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin    
    
    class Meta:
        db_table = "sys_user"
        
        
@python_2_unicode_compatible # Python 2.x 지원용
class SysMenu(models.Model):        
    """ 시스템 메뉴 ModelClass
    """
#    menu_id = models.CharField(db_column='menu_id', max_length=10, blank=True) # 메뉴ID
#    up_menu_id = models.CharField(db_column='up_menu_id', max_length=10, blank=True) # 상위메뉴ID
    menu_id = models.CharField(primary_key=True, db_column='menu_id', max_length=10, blank=True) # 메뉴ID
#    up_menu_id = models.ForeignKey('self', db_column='up_menu_id', null=True, blank=True) # 상위메뉴ID
    up_menu_id = models.ForeignKey('self', db_column='up_menu_id', blank=True, null=True, default=None, related_name='up_menu_id_menu_id') # 상위메뉴ID
    menu_nm = models.CharField(db_column='menu_nm', max_length=100, null=True, blank=True) # 메뉴명
    menu_desc = models.CharField(db_column='menu_desc', max_length=100, null=False, blank=True, default='') # 메뉴설명
    menu_url = models.CharField(db_column='menu_url', max_length=256, null=False, blank=False) # 메뉴링크
    menu_lvl = models.IntegerField(db_column='menu_lvl', null=False, default=1) # 메뉴레벨
    menu_auth = models.CharField(db_column='menu_auth', max_length=20, null=False, blank=True) # 메뉴권한(M: 시스템관리자, C: 대표, A:총괄, T:팀장, S:사원, I: 인턴)
    use_yn = models.CharField(db_column='use_yn', max_length=1, null=False, default='Y') # 사용여부
    reg_id  = models.CharField(db_column='reg_id', max_length=10, null=False, default='system') # 등록자ID
    reg_dt  = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True) # 등록일자
    mod_id  = models.CharField(db_column='mod_id', max_length=10, null=False, default='system') # 수정자ID
    mod_dt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True) # 수정일자
        
    class Meta:
        db_table = "sys_menu"
        unique_together = (("menu_id",),)
        
        