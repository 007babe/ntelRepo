from pprint import pprint

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, \
    UserCreationForm, UserChangeForm
from django.contrib.auth.hashers import make_password
from django.db.models.query_utils import Q
from django.forms.forms import Form
from django.forms.models import ModelForm
from django.utils.translation import gettext as _

from system.forms import SysUserCreationForm, SysUserChangeForm
from system.models import SysUser, SysCompany, SysShop
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
        instanceStaffModify.modId = SysUser.objects.get(userId__exact=self.request.user.userId)  # 수정자ID

        # 비밀번호가 입력되었을 경우
        if not is_empty(self.request.POST.get("password")):
            instanceStaffModify.password = make_password(self.request.POST.get("password"))

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
    직원정보 변경 Form
    '''
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # request 객체
        super(ShopModifyForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ShopModifyForm, self).clean()

    def save(self, commit=True):
        cleaned_data = super(ShopModifyForm, self).clean()
        instanceShopModify = super(ShopModifyForm, self).save(commit=False)

        instanceShopModify.modId = SysUser.objects.get(userId__exact=self.request.user.userId)  # 수정자ID

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



