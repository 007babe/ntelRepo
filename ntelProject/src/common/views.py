import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from common.models import ComCd
from src.common.utils.json import jsonDefault


@login_required(login_url='/accounts/login/')
def getJsonComCd(request):
    """
        공통코드(tb_com_cd) 데이터 획득(Json)
    """
    # 공통코드 데이터 획득
    comCds = ComCd.objects.filter(
        useYn=True,
    ).values(
        'grpCd', 
        'comCd', 
        'comNm', 
        'grpOpt',
        'useYn', 
    )
    jsonData = json.dumps(list(comCds), default=jsonDefault)
    return HttpResponse(jsonData, content_type="application/json")    





