from __future__ import unicode_literals  # Python 2.x 지원용

from django.db import models
from django.urls.base import reverse
from django.utils.encoding import python_2_unicode_compatible

from common.model.fields import ThumbnailImageField


@python_2_unicode_compatible # Python 2.x 지원용
class SampleAlbum(models.Model):
    """ 샘플앨범 ModelClass
    """
    name = models.CharField(db_column='name', max_length=50, verbose_name='앨범명') # 앨범명
    description = models.CharField(db_column='description', max_length=100, blank=True, verbose_name='album description') # 앨범설명
    
    # 속성
    class Meta:
        db_table="sample_album"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('sample:album_detail', args=(self.id,))
        
@python_2_unicode_compatible # Python 2.x 지원용
class SamplePhoto(models.Model):
    """ 샘플사진 ModelClass
    """
    album = models.ForeignKey(SampleAlbum)
    title = models.CharField(db_column='title', max_length=50, verbose_name='사진제목')
    image = ThumbnailImageField(upload_to='photo/%Y/%m')
    description = models.CharField(db_column='description', max_length=100, blank=True, verbose_name='photo description')
    upload_date = models.DateTimeField(db_column='upload_date', auto_now_add=True, verbose_name='업로드일자')
    
    # 속성
    class Meta:
        db_table="sample_photo"

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('sample:photo_detail', args=(self.id,))

