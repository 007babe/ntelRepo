# -*- coding: utf-8 -*-
'''
def my_custom_sql(self):
    cursor = connection.select_db("nteldb")
    
#    cursor = connection.cursor()
 
    cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
 
    cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
    row = cursor.fetchone()
 
    return row
'''
# Create your models here.


from django.db import models


class COM_CD(models.Model):
    grpCd  = models.CharField(max_length=5)
    comCd  = models.CharField(max_length=10)
    comNm  = models.CharField(max_length=100)
    ordSeq = models.IntegerField(default=1)
    useYn  = models.CharField(max_length=1, default="Y")
    grpOpt = models.CharField(max_length=100, null=True)
    regId  = models.CharField(max_length=10)
    regDt  = models.DateTimeField(auto_now_add=True)
    modId  = models.CharField(max_length=10)
    modDt  = models.DateTimeField(auto_now=True)
    
    # 속성
    class Meta:
        unique_together = (("grpCd", "comCd"),)
    
    def publish(self):
        self.save()
        
    def __unicode__(self):
        return models.Model.__str__(self)
