from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, \
    UserCreationForm, UserChangeForm

from system.models import SysUser


class SysUserCreationForm(UserCreationForm):
    # custom Form Field
    # 기존의 sex 필드를 대체함
    CHOICE = (('M', '남자'), ('W', '여자'))
    sex = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICE,
        label='성별'
    )

    class Meta:
        model = SysUser
        fields = ('user_id',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password don`t match')

        return password2

    def save(self, commit=True):
        # 비밀번호를 해시형태로 저장
        user = super(SysUserCreationForm, self).save(commit=False)
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
        fields = ('user_id',)
