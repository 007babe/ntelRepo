from __future__ import absolute_import

import json

from django.http import HttpResponse

from common.models import ComCd
from common.utils.ajax import login_required_ajax
from common.utils.json import jsonDefault


@login_required_ajax
def getJsonComCd(request):
    """
        공통코드(com_cd) 데이터 획득(Json)
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
