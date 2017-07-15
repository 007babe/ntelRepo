from django.contrib import admin

from common.models import ComCd


# Register your models here.
class CommonAdmin(admin.ModelAdmin):
    list_display = ('grpCd', 'comCd')

admin.site.register(ComCd, CommonAdmin)    
