# -*- coding: utf-8 -*-
import json

from django.core import serializers
from django.core.serializers.python import Serializer
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from common.models import COM_CD



#def ComCd(request, tab=None):
# Create your views here.
def index(request):
    
#    return HttpResponse("앗싸... 첫페이지 index")
    return render(request, 'main/main.html', {})

'''
공통코드 데이터 획득(json) 
'''
#@csrf_exempt
#def comCdDb(request):
#    Feedback.objects.all()

def jsonComCd(request):
    COM_CD.objects.all()


'''
공통코드 데이터 획득
'''
@csrf_exempt
def comCd(request):
    jsonData = serializers.serialize('json', COM_CD.objects.all(), fields=('grpCd', 'comCd', 'comNm', 'useYn', 'grpOpt'))    
    return HttpResponse(jsonData, content_type="application/json")    
    
