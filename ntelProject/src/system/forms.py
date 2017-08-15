from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, \
    UserCreationForm, UserChangeForm
from django.forms.models import ModelForm

from system.models import SysUser, SysCompany
from utils.data import getSysSeqId, isUsableId


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

        userAuth = self.user.userAuth_id
        shopId = self.user.shopId_id
        companyId = self.user.shopId.companyId_id
        
        
        
        # 등록 권한 체크
        if userAuth not in ["S0001M", "S0001C", "S0001A", "S0001T",]:  # 시스템관리자, 대표, 총괄, 팀장이 아닐 경우 등록 불가
            self.non_field_error(_('등록권한이 없습니다.'))

        if userAuth not in ["S0001M", "S0001C", "S0001A",]:  # 시스템관리자, 대표, 총괄이 아닐 경우 로그인 사용자의 매장ID로 세팅
            self.shopId = self.request.shopId
        else:
            pass

        # 사용가능한 ID인지 체크
        if not isUsableId(cleaned_data.get('userId')):
            self.add_error('userId', _('사용하실 수 없는 아이디입니다.'))

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


class SysUserChangeForm(UserChangeForm):
    # 유저 업데이트 폼
    # 모든 필드 포함, 비밀번호는 해시로 표시
    password = ReadOnlyPasswordHashField(label="비밀번호")

    class Meta:
        model = SysUser
        fields = ('userId',)
