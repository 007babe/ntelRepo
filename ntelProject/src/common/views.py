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
def getComCd(request):
    """
        공통코드(TB_COM_CD) 데이터 획득(Json)
    """
    jsonData = serializers.serialize('json', TbComCd.objects.all(), fields=('grpCd', 'comCd', 'comNm', 'useYn', 'grpOpt'))    
#    jsonData = serializers.serialize('json', TbComCd.objects.all(), fields=('grp_cd', 'com_cd', 'com_nm', 'useYn', 'grp_opt'))    
    return HttpResponse(jsonData, content_type="application/json")    
    
