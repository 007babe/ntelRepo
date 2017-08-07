import re

from django import forms
from django.contrib.auth.hashers import make_password
from django.forms.models import ModelForm
from django.utils.translation import gettext as _

from system.models import SysAppReq
from system.models import SysPolicy
from utils.data import getSysSeqId
from utils.data import isUsableId


class SysAppReqForm(ModelForm):
    '''
    이용신청 Form class
    '''
    # 신청ID
    reqId = forms.CharField(required=False)  # 신청ID는 신규생성이므로 Null=True
    # 이용정책ID
    policyId = forms.ModelChoiceField(queryset=SysPolicy.objects.all())
    # 이용약관동의
    confirmAccessTerms = forms.BooleanField(required=True)
    # 개인정보취급방침동의
    confirmPrivacyPolicy = forms.BooleanField(required=True)
    # 사용자ID
    userId = forms.CharField(required=False, min_length=6, max_length=20)
    # 비밀번호
    password = forms.CharField(widget=forms.PasswordInput(), min_length=6, max_length=20)
    # 비밀번호확인
    passwordChk = forms.CharField(widget=forms.PasswordInput(), min_length=6, max_length=20)
    # 이메일
    email = forms.EmailField(max_length=255)

    def __init__(self, *args, **kwargs):
        # 로그인 사용자 정보 활용
        # self.user = kwargs.pop('user', None)
        super(SysAppReqForm, self).__init__(*args, **kwargs)

        self.fields.keyOrder = [
            'confirmAccessTerms',
            'confirmPrivacyPolicy',
            'companyNm',
            'shopNm',
            'bizLicNo1',
            'bizLicNo2',
            'bizLicNo3',
            'telNo1',
            'telNo2',
            'telNo3',
            'userId',
            'password',
            'passwordChk',
            'email',
        ]

    def clean(self):
        cleaned_data = super(SysAppReqForm, self).clean()
        # 사용가능한 ID인지 체크
        if not isUsableId(cleaned_data.get('userId')):
            self.add_error('userId', _('사용하실 수 없는 아이디입니다.'))

        # 비밀번호 & 비밀번호 확인 일치 여부 체크
        password = cleaned_data.get('password')
        passwordChk = cleaned_data.get('passwordChk')
        if password != passwordChk:
            self.add_error('password', _('비밀번호확인과 일치하지 않습니다.'))

    def save(self, commit=True):
        cleaned_data = super(SysAppReqForm, self).clean()
        instance = super(SysAppReqForm, self).save(commit=False)
        # 신규 이용 신청 번호 획득 후 세팅
        self.reqId = getSysSeqId('APRQID')
        instance.reqId = self.reqId

        # 비밀번호 암호화
        instance.password = make_password(cleaned_data.get('password'))
        if commit:
            instance.save()
        return instance

    class Meta:
        model = SysAppReq
        fields = "__all__"
