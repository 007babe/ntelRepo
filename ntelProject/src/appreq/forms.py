import re

from django import forms
from django.contrib.auth.hashers import make_password
from django.db.models.expressions import Value
from django.forms.models import ModelForm
from django.utils.translation import gettext as _

from system.models import SysAppreq, SysComCd
from system.models import SysPolicy
from utils.data import getSysSeqId, is_empty
from utils.data import isUsableId


class SysAppreqRegistForm(ModelForm):
    '''
    이용신청(SysAppreq) 생성 Form class
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
    userId = forms.CharField(required=True, min_length=6, max_length=20)
    # 비밀번호
    password = forms.CharField(required=True, min_length=6, max_length=20)
    # 비밀번호확인
    passwordChk = forms.CharField(required=True, min_length=6, max_length=20)
    # 망별 통신사코드
    networkCompanyId = forms.CharField(required=False, max_length=100)
    # 이메일
    email = forms.EmailField(max_length=255)
    # 진행상태
    reqStatus = forms.CharField(required=False)  # 신청ID는 신규생성이므로 Null=True
    # 통신사
    networkCompanyIdD = forms.CharField(required=False)  #딜러점 통신사
    networkCompanyIdA = forms.CharField(required=False)  #대리점 통신사
    networkCompanyIdC = forms.CharField(required=False)  #유선사업 통신사

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(SysAppreqRegistForm, self).__init__(*args, **kwargs)

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
        cleaned_data = super(SysAppreqRegistForm, self).clean()

        # 사용가능한 ID인지 체크
        if not isUsableId(cleaned_data.get('userId')):
            self.add_error('userId', _('사용하실 수 없는 아이디입니다.'))

        # 비밀번호 & 비밀번호 확인 일치 여부 체크
        password = cleaned_data.get('password')
        passwordChk = cleaned_data.get('passwordChk')
        if password != passwordChk:
            self.add_error('password', _('비밀번호확인과 일치하지 않습니다.'))

        # 통신사 선택 체크
        companyTp = self.request.POST.get('companyTp')
        if companyTp == 'S0004D':  # 딜러점일 경우
            if is_empty(self.request.POST.getlist("networkCompanyIdD")):
                self.add_error('networkCompanyIdD', _('통신사를 선택해 주세요.'))
        elif companyTp == 'S0004A':  # 대리점일 경우
            if is_empty(self.request.POST.get("networkCompanyIdA")):
                self.add_error('networkCompanyIdA', _('통신사를 선택해 주세요.'))
        elif companyTp == 'S0004C':  # 유선사업일 경우
            if is_empty(self.request.POST.getlist("networkCompanyIdC")):
                self.add_error('networkCompanyIdC', _('통신사를 선택해 주세요.'))

    def save(self, commit=True):
        cleaned_data = super(SysAppreqRegistForm, self).clean()
        instanceSysAppreq = super(SysAppreqRegistForm, self).save(commit=False)

        # 신규 이용 신청 번호 획득 후 세팅
        self.reqId = getSysSeqId('APRQID')
        instanceSysAppreq.reqId = self.reqId

        # 회사등급 ('S0006A')  일반등급으로 세팅(comCd.grpCd='S0006' 참조)
        instanceSysAppreq.companyGrade = SysComCd.objects.get(comCd__exact='S0006A')

        # 진행상태 승인요청('S0008R')  세팅(comCd.grpCd='S0008' 참조)
        instanceSysAppreq.reqStatus = SysComCd.objects.get(comCd__exact='S0008A')

        # 비밀번호 암호화
        instanceSysAppreq.password = make_password(cleaned_data.get('password'))

        # 회사타입별 망별통신사 코드
        companyTp = self.request.POST.get('companyTp')
        if companyTp == 'S0004D':  # 딜러점일 경우
            instanceSysAppreq.networkCompanyId = ",".join(self.request.POST.getlist("networkCompanyIdD")) 
        elif companyTp == 'S0004A':  # 대리점일 경우
            instanceSysAppreq.networkCompanyId = self.request.POST.get("networkCompanyIdA")
        elif companyTp == 'S0004C':  # 유선사업일 경우
            instanceSysAppreq.networkCompanyId = ",".join(self.request.POST.getlist("networkCompanyIdC")) 

        if commit:
            instanceSysAppreq.save()
        return instanceSysAppreq

    class Meta:
        model = SysAppreq
        fields = "__all__"
