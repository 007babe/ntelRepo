from __future__ import unicode_literals  # Python 2.x 지원용

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User, PermissionsMixin
from django.db import models
from django.db.models.query_utils import Q
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible  # Python 2.x 지원용
class SysPolicy(models.Model):
    """엔텔 운영정책 회사 정보
    """
    accessTerms = models.TextField(db_column='access_terms', null=True, blank=True, default=None, verbose_name='이용약관')
    privacyPolicy = models.TextField(db_column='privacy_policy', null=True, blank=True, default=None, verbose_name='개인정보취급방법')
    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    class Meta:
        db_table = "sys_policy"

    def __str__(self):
        return str(self.id)

@python_2_unicode_compatible  # Python 2.x 지원용
class SysLoginHistory(models.Model):
    """사용자 로그인 이력
    """
    userId = models.ForeignKey('system.SysUser', on_delete=models.CASCADE, db_column='user_id', null=False, blank=False, related_name='r_%(app_label)s_%(class)s_user_id', verbose_name='사용자ID')
    loginDt = models.DateTimeField(db_column='login_dt', auto_now_add=True, null=False, blank=True, verbose_name='로그인일자')
    httpUserAgent = models.TextField(db_column='http_user_agent', null=True, blank=True, default=None, verbose_name='UserAgent정보')
    remoteAddr  = models.TextField(db_column='remote_addr', null=True, blank=True, default=None, verbose_name='접속 IP')
    remoteHost  = models.TextField(db_column='remote_host', null=True, blank=True, default=None, verbose_name='접속 Host')

    class Meta:
        db_table = "sys_login_history"

    def __str__(self):
        return str(self.id)


@python_2_unicode_compatible  # Python 2.x 지원용
class SysCompany(models.Model):
    """엔텔 사용 회사 정보
    고유발생 Key로 PK 설정
    """
    companyId = models.CharField(db_column='company_id', primary_key=True, max_length=10, blank=False, default=None, verbose_name='회사ID') # 회사ID
    companyNm = models.CharField(db_column='company_nm', max_length=100, null=False, blank=True, verbose_name='회사명') # 회사명
    companyTp = models.ForeignKey('common.ComCd', db_column='company_tp', null=True, blank=True, default=None, related_name='r_%(app_label)s_%(class)s_company_tp', verbose_name='회사구분') # ComCd.grpCd = 'S0004'
    companyGrade = models.ForeignKey('common.ComCd', db_column='company_grade', null=True, blank=True, default=None, related_name='r_%(app_label)s_%(class)s_company_grade', verbose_name='회사등급')  # ComCd.grpCd = 'S0006'
    isReal = models.BooleanField(db_column='is_real', null=False, blank=False, default=False, verbose_name='실회사구분')
    policyId = models.ForeignKey('system.SysPolicy', db_column='policy_id', null=True, blank=True, default=None, related_name='r_%(app_label)s_%(class)s_policy_id', verbose_name='이용약관ID')
    bizLicNo1 = models.CharField(db_column='biz_lic_no1', max_length=3, null=True, blank=True, verbose_name='사업자번호1')
    bizLicNo2 = models.CharField(db_column='biz_lic_no2', max_length=2, null=True, blank=True, verbose_name='사업자번호2')
    bizLicNo3 = models.CharField(db_column='biz_lic_no3', max_length=5, null=True, blank=True, verbose_name='사업자번호3')
    telNo1 = models.CharField(db_column='tel_no1', max_length=5, null=True, blank=True, default=None, verbose_name='회사전화1')
    telNo2 = models.CharField(db_column='tel_no2', max_length=5, null=True, blank=True, default=None, verbose_name='회사전화2')
    telNo3 = models.CharField(db_column='tel_no3', max_length=5, null=True, blank=True, default=None, verbose_name='회사전화3')
    faxNo1 = models.CharField(db_column='fax_no1', max_length=5, null=True, blank=True, default=None, verbose_name='회사FAX1')
    faxNo2 = models.CharField(db_column='fax_no2', max_length=5, null=True, blank=True, default=None, verbose_name='회사FAX2')
    faxNo3 = models.CharField(db_column='fax_no3', max_length=5, null=True, blank=True, default=None, verbose_name='회사FAX3')
    cellNo1 = models.CharField(db_column='cell_no1', max_length=5, null=True, blank=True, default=None, verbose_name='회사휴대폰1')
    cellNo2 = models.CharField(db_column='cell_no2', max_length=5, null=True, blank=True, default=None, verbose_name='회사휴대폰2')
    cellNo3 = models.CharField(db_column='cell_no3', max_length=5, null=True, blank=True, default=None, verbose_name='회사휴대폰3')
    bizTp = models.CharField(db_column='biz_tp', max_length=100, null=True, blank=True, verbose_name='업태')
    bizKind = models.CharField(db_column='biz_kind', max_length=100, null=True, blank=True, verbose_name='업종')
    zipCd = models.CharField(db_column='zip_cd', max_length=6, null=True, blank=True, verbose_name='회사우편번호') # 우편번호
    addr1 = models.TextField(db_column='addr_1', max_length=200, null=True, blank=True, verbose_name='회사기본주소') # 기본 주소
    addr2 = models.TextField(db_column='addr_2', max_length=200, null=True, blank=True, verbose_name='회사상세주소') # 상세주소
    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    class Meta:
        db_table = "sys_company"

    def __str__(self):
        return self.companyId


@python_2_unicode_compatible  # Python 2.x 지원용
class SysShop(models.Model):
    """엔텔 사용 매장 정보
    고유발생 Key로 PK 설정
    """
    shopId = models.CharField(db_column='shop_id', primary_key=True, max_length=12, blank=False, default=None, verbose_name='매장ID')
    companyId = models.ForeignKey('system.SysCompany', on_delete=models.CASCADE, db_column='company_id', blank=True, null=True, default=None, related_name='r_%(app_label)s_%(class)s_company_id')
    shopNm = models.CharField(db_column='shop_nm', max_length=100, blank=True, verbose_name='매장명')
    isMain = models.BooleanField(db_column='is_main', default=False, verbose_name='기본매장여부')
    telNo1 = models.CharField(db_column='tel_no1', max_length=5, null=True, blank=True, default=None, verbose_name='매장전화1')
    telNo2 = models.CharField(db_column='tel_no2', max_length=5, null=True, blank=True, default=None, verbose_name='매장전화2')
    telNo3 = models.CharField(db_column='tel_no3', max_length=5, null=True, blank=True, default=None, verbose_name='매장전화3')
    faxNo1 = models.CharField(db_column='fax_no1', max_length=5, null=True, blank=True, default=None, verbose_name='회사FAX1')
    faxNo2 = models.CharField(db_column='fax_no2', max_length=5, null=True, blank=True, default=None, verbose_name='회사FAX2')
    faxNo3 = models.CharField(db_column='fax_no3', max_length=5, null=True, blank=True, default=None, verbose_name='회사FAX3')
    cellNo1 = models.CharField(db_column='cell_no1', max_length=5, null=True, blank=True, default=None, verbose_name='매장휴대폰1')
    cellNo2 = models.CharField(db_column='cell_no2', max_length=5, null=True, blank=True, default=None, verbose_name='매장휴대폰2')
    cellNo3 = models.CharField(db_column='cell_no3', max_length=5, null=True, blank=True, default=None, verbose_name='매장휴대폰3')
    zipCd = models.CharField(db_column='zip_cd', max_length=6, blank=True, verbose_name='매장우편번호')
    addr1 = models.TextField(db_column='addr_1', max_length=200, blank=True, verbose_name='매장기본주소')
    addr2 = models.TextField(db_column='addr_2', max_length=200, blank=True, verbose_name='매장상세주소')
    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    class Meta:
        db_table = "sys_shop"

    def __str__(self):
        return self.shopId


@python_2_unicode_compatible  # Python 2.x 지원용
class SysUserManager(BaseUserManager):
    """
    시스템 사용자 관리 매니저
    """
    def create_user(self, userId, userNm, cellNo, email, password):
        """
        일반 사용자 생성
        """
        if not userId:
            raise ValueError('ID는 필수 입력입니다.')

        if not userNm:
            raise ValueError('이름은 필수 입력입니다.')

        if not cellNo:
            raise ValueError('휴대폰번호는 필수 입력입니다.')

        if not email:
            raise ValueError('email은 필수 입력입니다.')

        user = self.model(
            userId=userId,
            userNm=userNm,
            # email=self.nomalize_email(email),
        )

        user.is_admin = False
        user.set_password(password)
        user.save(using=self._db)
        return User

    def create_superuser(self, userId, userNm, password):
        """
        Superuser 사용자 생성(createsuperuser)
        """
        user = self.create_user(
            userId,
            userNm,
            password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def for_company(self, companyId):
        '''
        동일회사 데이터
        '''
        qry = Q()
        qry &= Q(shopId__companyId__exact=companyId)
        return self.get_queryset().filter(
            qry
        )

    def for_shop(self, shopId):
        '''
        동일매장 데이터
        '''
        qry = Q()
        qry &= Q(shopId__exact=shopId)
        return self.get_queryset().filter(
            qry
        )


@python_2_unicode_compatible  # Python 2.x 지원용
class SysUser(AbstractBaseUser, PermissionsMixin):
    """장고 User모델 Customized
    """
    userId = models.CharField(primary_key=True, db_column='user_id', max_length=20, verbose_name='아이디')
    userNm = models.CharField(db_column='user_nm', max_length=30, null=False, blank=False, verbose_name='사용자 이름')
    shopId = models.ForeignKey('system.SysShop', on_delete=models.CASCADE, db_column='shop_id', null=True, blank=True, default=None, related_name='r_%(app_label)s_%(class)s_shop_id', verbose_name='매장ID') # SysShop.shopId
    email = models.EmailField(db_column='email', max_length=255, null=True, blank=True, default=None, verbose_name='이메일')
    telNo1 = models.CharField(db_column='tel_no1', max_length=5, null=True, blank=True, default=None, verbose_name='전화1')
    telNo2 = models.CharField(db_column='tel_no2', max_length=5, null=True, blank=True, default=None, verbose_name='전화2')
    telNo3 = models.CharField(db_column='tel_no3', max_length=5, null=True, blank=True, default=None, verbose_name='전화3')
    cellNo1 = models.CharField(db_column='cell_no1', max_length=5, null=True, blank=True, default=None, verbose_name='휴대폰1')
    cellNo2 = models.CharField(db_column='cell_no2', max_length=5, null=True, blank=True, default=None, verbose_name='휴대폰2')
    cellNo3 = models.CharField(db_column='cell_no3', max_length=5, null=True, blank=True, default=None, verbose_name='휴대폰3')
    zipCd = models.CharField(db_column='zip_cd', max_length=7, null=True, blank=True, default=None, verbose_name='우편번호')
    addr1 = models.TextField(db_column='addr1', max_length=200, null=True, blank=True, default=None, verbose_name='주소1')
    addr2 = models.TextField(db_column='addr2', max_length=200, null=True, blank=True, default=None, verbose_name='주소2')
    userAuth = models.ForeignKey('common.ComCd', db_column='user_auth', null=True, blank=True, default=None, related_name='r_%(app_label)s_%(class)s_user_auth', verbose_name='사용자권한') # ComCd.grpCd = 'S0001'
    connLimit = models.CharField(db_column='conn_limit', max_length=10, null=True, blank=True, default=None, verbose_name='접속제한') # PC제한 : P, MOBILE제한 : M
    loginCnt = models.IntegerField(db_column='login_cnt', null=False, blank=True, default=0, verbose_name='로그인회수')
    useYn = models.BooleanField(db_column='use_yn', null=False, blank=True, default=False, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

#    is_active = models.BooleanField(default=True)
#    is_admin = models.BooleanField(default=False)

    # Model Manager
    objects = SysUserManager()

    # 유저 모델에서 필드의 이름을 설명하는 string. 유니크 식별자로 사용
    USERNAME_FIELD = 'userId'

    # createsuperuser 커맨드로 유저를 생성할 때 나타날 필드 이름 목록
    REQUIRED_FIELDS = ['userNm', 'password', 'email']  # 필수 입력 필드 정의


    @property
    def userAuthNm(self):
        '''
        사용자 권한 명(등급)
        '''
        return self.userAuth.comNm

    @property
    def shopNm(self):
        '''
        사용자 소속 매장명
        '''
        return self.shopId.shopNm

#    shopNm1 = property(_shopNm)

    def companyId(self):
        '''
        사용자 소속 회사ID
        '''
        return self.shopId.companyId

    def companyNm(self):
        '''
        사용자 소속 회사명
        '''
        return self.shopId.companyId.companyNm

    def companyTp(self):
        '''
        회사구분
        '''
        return self.shopId.companyId.companyTp

    def companyTpNm(self):
        '''
        회사구분명
        '''
        return self.shopId.companyId.companyTp.comNm

    def shopCnt(self):
        '''
        회사의 매장 수
        '''
        return SysShop.objects.filter(
            companyId__exact=self.companyId(),
            useYn__exact=True
        ).count()

    def staffCnt(self):
        '''
        매장의 직원 수
        '''
        return SysUser.objects.filter(
            shopId__exact=self.shopId,
            useYn__exact=True
        ).count()

    def __str__(self):
        return self.userId

    class Meta:
        db_table = "sys_user"


@python_2_unicode_compatible  # Python 2.x 지원용
class SysMenu(models.Model):
    """
    시스템 메뉴 ModelClass
    """
    menuId = models.CharField(primary_key=True, db_column='menu_id', max_length=10, blank=True, verbose_name='메뉴ID') # 메뉴ID
    upMenuId = models.ForeignKey('self', db_column='up_menu_id', blank=True, null=True, related_name='r_%(app_label)s_%(class)s_menu_id', on_delete=models.CASCADE, verbose_name='상위메뉴ID') # 상위메뉴ID
    menuNm = models.CharField(db_column='menu_nm', max_length=100, null=True, blank=True, verbose_name='메뉴명') # 메뉴명
    menuTmp = models.CharField(db_column='menu_tmp', max_length=512, null=True, blank=True, default=None, verbose_name='메뉴템플릿') # 메뉴템플릿
    menuLvl = models.IntegerField(db_column='menu_lvl', null=False, default=1, verbose_name='메뉴레벨') # 메뉴레벨
    menuCss = models.CharField(db_column='menu_css', max_length=200, null=True, blank=True, verbose_name='메뉴CSS') # 메뉴CSS
    menuDesc = models.CharField(db_column='menu_desc', max_length=200, null=False, blank=True, default='', verbose_name='메뉴설명') # 메뉴설명
    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    class Meta:
        db_table = "sys_menu"

    def __str__(self):
        return self.menuId

    def as_dict(self):
        return {
            "menuId": self.menuId,
            "upMenuId": self.upMenuId,
            "menuNm": self.menuNm,
            "menuTmp": self.menuTmp,
            "menuLvl": self.menuLvl,
            "menuCss": self.menuCss,
            "menuDesc": self.menuDesc,
            "useYn": self.useYn,
            "regId": self.regId,
            "modId": self.modId,
            "modDt": self.modDt,
        }

    def upMenuNm(self):
        '''
        상위 메뉴명
        '''
        return self.upMenuId.menuNm

    def topMenuNm(self):
        '''
        최상위 메뉴명
        '''
        topMenuNm = ''
        if self.menuLvl == 3:
            topMenuNm = self.upMenuId.upMenuId.menuNm
        if self.menuLvl == 2:
            topMenuNm = self.upMenuId.menuNm

        return topMenuNm

    def upMenuCss(self):
        '''
        상위 메뉴 Css
        '''
        return self.upMenuId.menuCss


@python_2_unicode_compatible  # Python 2.x 지원용
class SysMenuAuth(models.Model):
    """
    시스템 메뉴 권한 ModelClass
    """
    menuId = models.ForeignKey('system.SysMenu', db_column='menu_id', related_name='r_%(app_label)s_%(class)s_menu_id', on_delete=models.CASCADE, verbose_name='메뉴ID')
    menuAuth = models.ForeignKey('common.ComCd', db_column='menu_auth', related_name='r_%(app_label)s_%(class)s_menu_auth', verbose_name='메뉴권한')
    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    class Meta:
        db_table = "sys_menu_auth"
        unique_together = (("menuId", "menuAuth"),)

    def __str__(self):
        return self.menuId


@python_2_unicode_compatible  # Python 2.x 지원용
class SysMenuCompanyTp(models.Model):
    """
    시스템 메뉴 회사타입 ModelClass
    """
    menuId = models.ForeignKey('system.SysMenu', db_column='menu_id', related_name='r_%(app_label)s_%(class)s_menu_id', on_delete=models.CASCADE, verbose_name='메뉴ID' )
    companyTp = models.ForeignKey('common.ComCd', db_column='company_tp', related_name='r_%(app_label)s_%(class)s_company_tp', verbose_name='메뉴회사타입')
    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    class Meta:
        db_table = "sys_menu_company_tp"
        unique_together = (("menuId", "companyTp"),)

    def __str__(self):
        return self.menuId


@python_2_unicode_compatible  # Python 2.x 지원용
class SysMsg(models.Model):
    """엔텔 시스템 사용 메세지
    """
    msgCd = models.CharField(primary_key=True, db_column='msg_cd', max_length=6, verbose_name='메세지코드')
    msgTp = models.ForeignKey('common.ComCd', db_column='msg_tp', null=True, blank=True, default=None, related_name='r_%(app_label)s_%(class)s_msg_tp', verbose_name='메세지타입') # grpCd : S0007
    title = models.CharField(db_column='title', max_length=100, null=False, blank=False, default=None, verbose_name='메세지제목') # 메세지제목
    msg = models.CharField(db_column='msg', max_length=500, null=False, blank=False, default=None, verbose_name='메세지내용') # 메세지내용
    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    # 속성
    class Meta:
        db_table = "sys_msg"

    def publish(self):
        self.save()

    def __str__(self):
        return self.comCd


@python_2_unicode_compatible  # Python 2.x 지원용
class PublishedManager(models.Manager):
    '''기본 매니저
    '''
    use_for_related_fields = True

    def pulished(self, **kwargs):
        return self.filter(status='published', **kwargs)


@python_2_unicode_compatible  # Python 2.x 지원용
class SysAppreq(models.Model):
    """이용신청정보
    고유발생 Key로 PK 설정
    """
    objects = PublishedManager()

    reqId = models.CharField(db_column='req_id', primary_key=True, null=False, blank=False, max_length=10, verbose_name='요청ID') # 요청ID
    policyId = models.ForeignKey('system.SysPolicy', db_column='policy_id', null=False, blank=False, default=None, related_name='r_%(app_label)s_%(class)s_policy_id', verbose_name='이용약관ID')
    companyId = models.ForeignKey('system.SysCompany', on_delete=models.CASCADE, db_column='company_id', null=True, blank=True, default=None, related_name='r_%(app_label)s_%(class)s_company_cd', verbose_name='회사코드')
    companyNm = models.CharField(db_column='company_nm', max_length=100, null=False, blank=False, verbose_name='회사명')
    companyTp = models.ForeignKey('common.ComCd', db_column='company_tp', null=True, blank=True, default=None, related_name='r_%(app_label)s_%(class)s_company_tp', verbose_name='회사구분') # ComCd.grpCd = 'S0004'
    companyGrade = models.ForeignKey('common.ComCd', db_column='company_grade', null=True, blank=True, default=None, related_name='r_%(app_label)s_%(class)s_company_grade', verbose_name='회사등급')  # ComCd.grpCd = 'S0006'
    shopNm = models.CharField(db_column='shop_nm', max_length=100, null=False, blank=False, verbose_name='대표매장명')
    bizLicNo1 = models.CharField(db_column='biz_lic_no1', max_length=3, null=True, blank=True, verbose_name='사업자번호1')
    bizLicNo2 = models.CharField(db_column='biz_lic_no2', max_length=2, null=True, blank=True, verbose_name='사업자번호2')
    bizLicNo3 = models.CharField(db_column='biz_lic_no3', max_length=5, null=True, blank=True, verbose_name='사업자번호3')
    telNo1 = models.CharField(db_column='tel_no1', max_length=5, null=True, blank=True, default=None, verbose_name='회사전화1')
    telNo2 = models.CharField(db_column='tel_no2', max_length=5, null=True, blank=True, default=None, verbose_name='회사전화2')
    telNo3 = models.CharField(db_column='tel_no3', max_length=5, null=True, blank=True, default=None, verbose_name='회사전화3')
    cellNo1 = models.CharField(db_column='cell_no1', max_length=5, null=False, blank=False, default=None, verbose_name='대표자휴대폰1')
    cellNo2 = models.CharField(db_column='cell_no2', max_length=5, null=False, blank=False, default=None, verbose_name='대표자휴대폰2')
    cellNo3 = models.CharField(db_column='cell_no3', max_length=5, null=False, blank=False, default=None, verbose_name='대표자휴대폰3')
    bizTp = models.CharField(db_column='biz_tp', max_length=100, null=True, blank=True, verbose_name='업태')
    bizKind = models.CharField(db_column='biz_kind', max_length=100, null=True, blank=True, verbose_name='업종')
    zipCd = models.CharField(db_column='zip_cd', max_length=6, blank=True, verbose_name='회사우편번호') # 우편번호
    addr1 = models.TextField(db_column='addr_1', max_length=200, blank=True, verbose_name='회사기본주소') # 기본 주소
    addr2 = models.TextField(db_column='addr_2', max_length=200, blank=True, verbose_name='회사상세주소') # 상세주소
    userId = models.CharField(db_column='user_id', max_length=20, null=False, blank=False, default=None, verbose_name='대표사용자아이디')
    userNm = models.CharField(db_column='user_nm', max_length=30, null=False, blank=False, default=None, verbose_name='대표사용자명')
    password = models.CharField(db_column='password', max_length=128, null=False, blank=False, verbose_name='대표사용자비밀번호')
    email = models.EmailField(db_column='email', max_length=255, null=True, blank=True, default=None, verbose_name='이메일')
    reqStatus = models.ForeignKey('common.ComCd', db_column='req_status', null=True, blank=True, default=None, related_name='r_%(app_label)s_%(class)s_req_status', verbose_name='요청진행상태') # ComCd.grpCd = 'S0008'
    reqDt = models.DateTimeField(db_column='req_dt', auto_now_add=True, null=True, blank=True, verbose_name='요청일자')
    appDt = models.DateTimeField(db_column='app_dt', null=True, blank=True, verbose_name='승인일자')
    useYn = models.BooleanField(db_column='use_yn', null=False, blank=False, default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    class Meta:
        db_table = "sys_appreq"
        unique_together = (("userId"),)

    def __str__(self):
        return self.reqId


class SysSeq(models.Model):
    """시스템 코드 or Sequence 용
    """
    seqCd = models.CharField(primary_key=True, db_column='seq_cd', max_length=6, verbose_name='SEQ코드')
    seq = models.IntegerField(db_column='seq', null=False, blank=False, default=0, verbose_name='순차번호')
    seqLen =models.IntegerField(db_column='seq_len', null=False, blank=False, default=10, verbose_name='SEQ 길이')
    seqPrefix = models.CharField(db_column='seq_prefix', null=True, blank=True, default=None, max_length=3,  verbose_name='SEQ Prefix')
    useYm = models.BooleanField(db_column='use_ym', null=False, blank=True, default=False,  verbose_name='SEQ 년월사용여부')
    seqDesc = models.CharField(db_column='seq_desc', null=True, blank=True, default=None, max_length=100,  verbose_name='SEQ 설명')
    useYn = models.BooleanField(db_column='use_yn', default=True, verbose_name='사용여부')
    regId = models.ForeignKey('system.SysUser', db_column='reg_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_reg_id', verbose_name='등록자ID')
    regDt = models.DateTimeField(db_column='reg_dt', auto_now_add=True, null=True, blank=True, verbose_name='등록일자')
    modId = models.ForeignKey('system.SysUser', db_column='mod_id', null=True, blank=True, related_name='r_%(app_label)s_%(class)s_mod_id', verbose_name='수정자ID')
    modDt = models.DateTimeField(db_column='mod_dt', auto_now=True, blank=True, verbose_name='수정일자')

    class Meta:
        db_table = "sys_seq"

    def __str__(self):
        return self.id
