from django.contrib import admin

from sample.models import SamplePhoto, SampleAlbum


# Register your models here.
class PhotoInline(admin.StackedInline):
    model = SamplePhoto
    extra = 2
    
class SampleAlbumAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]
    list_display = ('name', 'description')
    
class SamplePhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'upload_date')
    
    
admin.site.register(SampleAlbum, SampleAlbumAdmin)
admin.site.register(SamplePhoto, SamplePhotoAdmin)

    