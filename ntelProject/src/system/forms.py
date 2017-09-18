from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, \
    UserCreationForm, UserChangeForm
from django.forms.models import ModelForm
from django.utils.translation import gettext as _

from system.models import SysUser, SysCompany
from utils.data import getSysSeqId


class SysCompanyForm(ModelForm):
    '''
    SysCompany등록 폼
    '''
    def __init__(self, *args, **kwargs):
        super(SysCompanyForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(SysCompanyForm, self).clean()

    def save(self, commit=True):
        cleaned_data = super(SysCompanyForm, self).clean()
        instance = super(SysCompanyForm, self).save(commit=False)

        self.companyId = getSysSeqId('SELLID')
        instance.companyId = self.companyId

        if commit:
            instance.save()

    class Meta:
        model = SysCompany
        fields = "__all__"


class SysUserCreationForm(UserCreationForm):
    '''
    사용자(SysUser) 등록 Form Class
    '''
    # 사용자ID
    userId = forms.CharField(required=True, min_length=6, max_length=20)
    # 비밀번호
    password = forms.CharField(min_length=6, max_length=20)
    # 비밀번호확인
    passwordChk = forms.CharField(widget=forms.PasswordInput(), min_length=6, max_length=20)
    # 이메일
    email = forms.EmailField(max_length=255)

    def __init__(self, *args, **kwargs):
        '''
        폼 초기화
        '''
        self.request = kwargs.pop('request', None)

    def clean(self):
        cleaned_data = super(SysUserCreationForm, self).clean()

        # 비밀번호 & 비밀번호 확인 일치 여부 체크
        '''
        password = cleaned_data.get('password')
        passwordChk = cleaned_data.get('passwordChk')
        if password != passwordChk:
            self.add_error('password', _('비밀번호확인과 일치하지 않습니다.'))
        '''

    class Meta:
        model = SysUser
        fields = ('userId',)

    def clean_password2(self):
        '''
        비밀번호와 비밀번호확인의 일치여부
        '''
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('passwordChk')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('비밀번호확인과 일치하지 않습니다.')

        return password2

    def save(self, commit=True):
        # 비밀번호를 해시형태로 저장
        user = super(SysUserCreationForm, self).save(commit=False)

        loginUserId = self.request.user.userId
        shopId = self.request.user.shopId_id
        companyId = self.request.user.shopId.companyId_id

        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user


class SysUserChangeShopForm(ModelForm):
    '''
    사용자 매장 변경 Form
    '''
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # request 객체
        super(SysUserChangeShopForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(SysUserChangeShopForm, self).clean()

    def save(self, commit=True):
        cleaned_data = super(SysUserChangeShopForm, self).clean()
        instanceUserChangeShop = super(SysUserChangeShopForm, self).save(commit=False)

        if commit:
            instanceUserChangeShop.save()
        return instanceUserChangeShop

    class Meta:
        model = SysUser
        fields = [
            "shopId",
        ]


class SysUserChangeForm(UserChangeForm):
    # 유저 업데이트 폼
    # 모든 필드 포함, 비밀번호는 해시로 표시
    password = ReadOnlyPasswordHashField(label="비밀번호")

    def __init__(self, *args, **kwargs):
        super(SysUserChangeForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(SysUserChangeForm, self).clean()

    class Meta:
        model = SysUser
        fields = ('userId',)


class SysPasswordChangeForm(forms.Form):
    '''
    비밀번호 변경 Form
    '''
    newPassword = forms.CharField(
        min_length=6,
        max_length=20,
    )
    newPasswordChk = forms.CharField(
        min_length=6,
        max_length=20,
    )

    field_order = [
        'newPassword',
        'newPasswordChk',
    ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # request 객체
        super(SysPasswordChangeForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(SysPasswordChangeForm, self).clean()

        # 비밀번호 & 비밀번호 확인 일치 여부 체크
        password = cleaned_data.get('newPassword')
        passwordChk = cleaned_data.get('newPasswordChk')
        if password != passwordChk:
            self.add_error('newPassword', _('비밀번호확인과 일치하지 않습니다.'))

    def save(self, commit=True):
        password = self.cleaned_data["newPassword"]
        self.request.user.set_password(password)

        self.request.user.modId = self.request.user

        if commit:
            self.request.user.save()
        return self.request.user

    class Meta:
        model = SysUser
