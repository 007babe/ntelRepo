from django.contrib.auth import admin
from django.contrib.auth.admin import UserAdmin

from system.forms import SysUserChangeForm, SysUserCreationForm
from system.models import SysUser


# Register your models here.
class SysUserAdmin(UserAdmin):
    # 필드들은 유저 모델을 표시하는데 사용됩니다.
    #  auth.User의 특정 필드를 참조하는 UserAdmin을 오버라이드합니다.

    # 회원 업데이트 폼 연결
    form = SysUserChangeForm
    list_display = ('user_id', 'username', 'tel_no', 'cell_no', 'email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        ('아이디', {'fields': ('user_id', 'password')}),
        ('개인 정보', {'fields': ('username', 'birthday', 'sex', 'email', 'phone')}),
        ('권한', {'fields': ('is_staff',)}),
    )

    # 회원 추가 폼 연결
    add_form = SysUserCreationForm
    add_fieldsets = (
        ('기본 정보', {'fields': ('user_id', 'password1', 'password2')}),
        ('추가 정보', {'fields': ('username', 'email', 'cell_no')})
    )

    search_fields = ('user_id', 'username',)
    ordering = ('username',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(SysUser, SysUserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
#admin.site.unregister(Group)