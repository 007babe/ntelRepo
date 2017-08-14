from __future__ import absolute_import

import json

from django.http import HttpResponse
from django.shortcuts import render

from common.models import ComCd, ComHttpStatus
from utils.ajax import login_required_ajax
from utils.json import jsonDefault
from utils.json import makeJsonResult


def errorPopupCV(request):
    '''
    공통 Error 팝업
    '''
    return render(
        request,
        'common/errors/errorPopup.html',
        {}
    )


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
    ).order_by(
        'grpCd',
        'ordSeq',
    )

    return HttpResponse(
        json.dumps(
            makeJsonResult(
                resultData=list(comCds)
            ),
            default=jsonDefault
        ),
        content_type="application/json"
    )


def getJsonComHttpStatus(request):
    """
        Http Status(com_http_status) 데이터 획득(Json)
    """
    comHttpStatuses = ComHttpStatus.objects.filter(
        useYn=True,
    ).values(
        'status',
        'title',
        'message',
        'useYn',
    )

    return HttpResponse(
        json.dumps(
            makeJsonResult(
                resultData=list(comHttpStatuses)
            ),
            default=jsonDefault
        ),
        content_type="application/json"
    )
