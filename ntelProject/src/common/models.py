# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from test.test_imageop import MAX_LEN

from _mysql import connection
from django.db import models


# Create your models here.
class ComCd(models.Model):
    grpCd  = models.CharField(max_length=5)
    comCd  = models.CharField(max_length=10)
    comNm  = models.CharField(max_length=100)
    ordSeq = models.IntegerField
    useYn  = models.CharField(max_length=1)
    grpOpt = models.CharField(max_length=100)
    regId  = models.CharField(max_length=10)
    regDt  = models.DateTimeField
    modId  = models.CharField(max_length=10)
    modDt  = models.DateTimeField
    
    
def my_custom_sql(self):
    cursor = connection.cursor()
 
    cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
 
    cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
    row = cursor.fetchall()
 
    return row    
    