from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from common.models import TbComCd


#def ComCd(request, tab=None):
# Create your views here.
def index(request):
    return render(request, 'main/main.html', {})

@csrf_exempt
@login_required(login_url='/accounts/login/')
def getComCd(request):
    """
        공통코드(TB_COM_CD) 데이터 획득(Json)
    """
    jsonData = serializers.serialize('json', TbComCd.objects.all(), fields=('grpCd', 'comCd', 'comNm', 'useYn', 'grpOpt'))   
    
    return HttpResponse(jsonData, content_type="application/json")    
    
