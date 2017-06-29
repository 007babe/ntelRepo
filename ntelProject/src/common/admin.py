from django.contrib import admin

from common.models import TbComCd


# Register your models here.
class CommonAdmin(admin.ModelAdmin):
    list_display = ('grpCd', 'comCd')

admin.site.register(TbComCd, CommonAdmin)    
