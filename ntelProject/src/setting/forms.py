from pprint import pprint

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, \
    UserCreationForm, UserChangeForm
from django.contrib.auth.hashers import make_password
from django.db.models.query_utils import Q
from django.forms.forms import Form
from django.forms.models import ModelForm
from django.utils.translation import gettext as _

from common.models import ComCd
from system.forms import SysUserCreationForm, SysUserChangeForm
from system.models import SysUser, SysCompany, SysShop, SysCompanyAccount
from utils.data import getSysSeqId, isUsableId, is_empty, getSysShopId


class StaffModifyForm(ModelForm):
    '''
    직원정보 변경 Form
    '''
    password = forms.CharField(required=False, min_length=6, max_length=20)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # request 객체
        super(StaffModifyForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(StaffModifyForm, self).clean()

    def save(self, commit=True):
        cleaned_data = super(StaffModifyForm, self).clean()
        instanceStaffModify = super(StaffModifyForm, self).save(commit=False)

        instanceStaffModify.connLimit = "".join(self.request.POST.getlist("connLimit"))  # 접속제한

        # 비밀번호가 입력되었을 경우
        if not is_empty(self.request.POST.get("password")):
            instanceStaffModify.password = make_password(self.request.POST.get("password"))

        instanceStaffModify.modId = self.request.user  # 수정자ID

        if commit:
            instanceStaffModify.save()
        return instanceStaffModify

    class Meta:
        model = SysUser
        fields = [
            "email",
            "userNm",
            "shopId",
            "addr1",
            "modId",
            "cellNo1",
            "cellNo2",
            "cellNo3",
            "userAuth",
            "connLimit",
            "useYn",
        ]


class StaffRegistForm(ModelForm):
    '''
    직원 등록 Form
    '''
    # 사용자ID
    userId = forms.CharField(required=True, min_length=6, max_length=20)
    # 비밀번호
    password = forms.CharField(required=True, min_length=6, max_length=20)
    # 비밀번호확인
    passwordChk = forms.CharField(required=True, min_length=6, max_length=20)
    # 이메일
    email = forms.EmailField(max_length=255)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(StaffRegistForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'userId',
            'password',
            'passwordChk',
            'userNm',
            'cellNo1',
            'cellNo2',
            'cellNo3',
            'addr1',
            'email',
        ]

    def clean(self):
        cleaned_data = super(StaffRegistForm, self).clean()

        # 등록 가능한 매장 인지 확인(등록자 회사 또는 매장)
        if self.request.user.userAuth_id in ["S0001M", "S0001C", "S0001A"]:  # 시스템관리자, 대표, 총괄일 경우
            shops = SysShop.objects.for_company(self.request.user.shopId.companyId).filter(
                shopId__exact=cleaned_data.get('shopId')
            )
            if shops.count() < 1:
                self.add_error('shopId', _('사용자를 등록할 수 없는 매장입니다.'))
        elif self.request.user.userAuth_id in ["S0001T"]:  # 점장
            if cleaned_data.get('shopId').shopId != self.request.user.shopId_id:
                self.add_error('shopId', _('사용자를 등록할 수 없는 매장입니다.'))
        else:
            self.add_error('__all__', _('사용자를 등록할 수 없습니다.'))

        # 사용가능한 ID인지 체크
        if not isUsableId(cleaned_data.get('userId')):
            self.add_error('userId', _('사용하실 수 없는 아이디입니다.'))

        # 비밀번호 & 비밀번호 확인 일치 여부 체크
        password = cleaned_data.get('password')
        passwordChk = cleaned_data.get('passwordChk')
        if password != passwordChk:
            self.add_error('password', _('비밀번호확인과 일치하지 않습니다.'))

    def save(self, commit=True):
        cleaned_data = super(StaffRegistForm, self).clean()
        instanceStaffRegist = super(StaffRegistForm, self).save(commit=False)

        # 접속제한 설정
        instanceStaffRegist.connLimit = "".join(self.request.POST.getlist("connLimit"))

        # 비밀번호 암호화
        instanceStaffRegist.password = make_password(cleaned_data.get('password'))

        # 등록자 ID
        instanceStaffRegist.regId = self.request.user
        # 수정자 ID
        instanceStaffRegist.modId = self.request.user

        if commit:
            instanceStaffRegist.save()
        return instanceStaffRegist

    class Meta:
        model = SysUser
        fields = "__all__"


class ShopModifyForm(ModelForm):
    '''
    매장정보 변경 Form
    '''
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # request 객체
        super(ShopModifyForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ShopModifyForm, self).clean()

    def save(self, commit=True):
        cleaned_data = super(ShopModifyForm, self).clean()
        instanceShopModify = super(ShopModifyForm, self).save(commit=False)

        instanceShopModify.modId = self.request.user  # 수정자ID

        if commit:
            instanceShopModify.save()
        return instanceShopModify

    class Meta:
        model = SysShop
        fields = [
            "shopNm",
            "telNo1",
            "telNo2",
            "telNo3",
            "faxNo1",
            "faxNo2",
            "faxNo3",
            "cellNo2",
            "cellNo3",
            "cellNo1",
            "cellNo2",
            "cellNo3",
            "addr1",
            "useYn",
        ]


class ShopRegistForm(ModelForm):
    '''
    매장 등록 Form
    '''
    # 매장ID
    shopId = forms.CharField(required=False)  # 매장등록은 신규생성이므로 Null=True

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ShopRegistForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'shopNm',
            'telNo1',
            'telNo2',
            'telNo3',
            'faxNo1',
            'faxNo2',
            'faxNo3',
            'cellNo1',
            'cellNo2',
            'cellNo3',
            'addr1',
        ]

    def clean(self):
        cleaned_data = super(ShopRegistForm, self).clean()
        # 회사등급에 따른 처리(기본형: 1매장, 고급형:3매장, 최고급형:무제한)

    def save(self, commit=True):
        cleaned_data = super(ShopRegistForm, self).clean()
        instanceShopRegist = super(ShopRegistForm, self).save(commit=False)

        # 매장번호 획득 후 세팅
        instanceShopRegist.shopId = getSysShopId(self.request.user.shopId.companyId)
        # 회사ID 세팅
        instanceShopRegist.companyId = self.request.user.shopId.companyId
        # 등록자 ID
        instanceShopRegist.regId = self.request.user
        # 수정자 ID
        instanceShopRegist.modId = self.request.user

        if commit:
            instanceShopRegist.save()
        return instanceShopRegist

    class Meta:
        model = SysShop
        fields = "__all__"


class CompanyAccountRegistForm(ModelForm):
    '''
    거래처 회사 연결 등록 Form
    '''
    companyId = forms.CharField(required=False)  # 회사 ID
    accountId = forms.CharField(required=False)  # 거래처 ID

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CompanyAccountRegistForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(CompanyAccountRegistForm, self).clean()

    def save(self, commit=True):
        cleaned_data = super(CompanyAccountRegistForm, self).clean()
        instanceCompanyAccountRegist = super(CompanyAccountRegistForm, self).save(commit=False)

        if commit:
            instanceCompanyAccountRegist.save()
        return instanceCompanyAccountRegist

    class Meta:
        model = SysCompanyAccount
        fields = "__all__"


class AccountRegistForm(ModelForm):
    '''
    거래처 등록 Form
    '''
    # 회사ID
    companyId = forms.CharField(required=False)  # 회사등록은 신규생성이므로 Null=True

    # 담당자명
    chargerNm = forms.CharField(required=True)

    # 사용여부
    useYn = forms.BooleanField(required=False)

    # 통신사코드
    networkCompanyId = forms.CharField(required=False, max_length=100)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(AccountRegistForm, self).__init__(*args, **kwargs)

        self.fields.keyOrder = [
            'companyNm',
            'companyTp',
            'networkCompanyId',
            'chargerNm',
            'telNo1',
            'telNo2',
            'telNo3',
            'faxNo1',
            'faxNo2',
            'faxNo3',
            'cellNo1',
            'cellNo2',
            'cellNo3',
            'addr1',
            'bizLicNo1',
            'bizLicNo2',
            'bizLicNo3',
            'bizTp',
            'bizKind',
            'useYn',
        ]

    def clean(self):
        cleaned_data = super(AccountRegistForm, self).clean()

    def save(self, commit=True):
        cleaned_data = super(AccountRegistForm, self).clean()
        instanceAccountRegist = super(AccountRegistForm, self).save(commit=False)

        # 회사코드 획득 후 세팅(거래처 "S0004T")
        instanceAccountRegist.companyId = getSysSeqId("S0004T")

        # 회사등급 ('S0006A')  일반등급으로 세팅(comCd.grpCd='S0006' 참조)
        instanceAccountRegist.companyGrade = ComCd.objects.get(comCd__exact='S0006A')

        # 회사타입별 통신사 코드
        companyTp = self.request.POST.get('companyTp')
        if companyTp == 'S0004D':  # 딜러점일 경우
            instanceAccountRegist.networkCompanyId = ",".join(self.request.POST.getlist("networkCompanyIdD")) 
        elif companyTp == 'S0004A':  # 대리점일 경우
            instanceAccountRegist.networkCompanyId = self.request.POST.get("networkCompanyIdA")

        # 실제 회사가 아님
        instanceAccountRegist.isReal = False

        # SysCompany 등록시는 사용 = True
        instanceAccountRegist.useYn = True

        # 등록자 ID
        instanceAccountRegist.regId = self.request.user

        # 수정자 ID
        instanceAccountRegist.modId = self.request.user

        if commit:
            instanceAccountRegist.save()
        return instanceAccountRegist

    class Meta:
        model = SysCompany
        fields = "__all__"


class AccountModifyForm(ModelForm):
    '''
    거래처 수정 Form
    '''
    # 담당자명
    chargerNm = forms.CharField(required=True)

    # 망별 통신사코드
    networkCompanyId = forms.CharField(required=False, max_length=100)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # request 객체
        super(AccountModifyForm, self).__init__(*args, **kwargs)

        self.fields.keyOrder = [
            'companyNm',
            'companyTp',
            'networkCompanyId',
            'chargerNm',
            'telNo1',
            'telNo2',
            'telNo3',
            'faxNo1',
            'faxNo2',
            'faxNo3',
            'cellNo1',
            'cellNo2',
            'cellNo3',
            'addr1',
            'bizLicNo1',
            'bizLicNo2',
            'bizLicNo3',
            'bizTp',
            'bizKind',
            'useYn',
        ]

    def clean(self):
        cleaned_data = super(AccountModifyForm, self).clean()

    def save(self, commit=True):
        cleaned_data = super(AccountModifyForm, self).clean()
        instanceAccountModify = super(AccountModifyForm, self).save(commit=False)

        # 회사타입별 통신사 코드
        companyTpSrtCd = instanceAccountModify.companyTp.srtCd
        if companyTpSrtCd == 'D':  # 딜러점일 경우
            instanceAccountModify.networkCompanyId = ",".join(self.request.POST.getlist("networkCompanyIdD"))
        elif companyTpSrtCd == 'A':  # 대리점일 경우
            instanceAccountModify.networkCompanyId = self.request.POST.get("networkCompanyIdA")

        # 수정자 ID
        instanceAccountModify.modId = self.request.user  # 수정자ID

        if commit:
            instanceAccountModify.save()

        return instanceAccountModify

    class Meta:
        model = SysCompany
        fields = [
            "companyNm",
            "networkCompanyId",
            "chargerNm",
            "telNo1",
            "telNo2",
            "telNo3",
            "faxNo1",
            "faxNo2",
            "faxNo3",
            "cellNo2",
            "cellNo3",
            "cellNo1",
            "cellNo2",
            "cellNo3",
            "bizLicNo1",
            "bizLicNo2",
            "bizLicNo3",
            "addr1",
            "bizTp",
            "bizKind",
            "modId",
        ]
