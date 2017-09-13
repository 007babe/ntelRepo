from __future__ import absolute_import

import json

from django.http import HttpResponse
from django.http.response import Http404

from telecom.models import TelecomNetworkCompany
from utils.json import jsonDefault, makeJsonDump
from utils.json import makeJsonResult


def getJsonTelecomNetworkCompany(request):
    """
        시스템 통신망별 통신사(telecom_network_telecom) 데이터 획득(Json)
    """
    if request.method == 'POST':
        telecomNetworkCompany = TelecomNetworkCompany.objects.for_order(
            useYn=True,
        ).values(
            'networkCompanyId',
            'networkCompanyNm',
            'networkId',
            'companyId',
            'useYn',
        )

        return HttpResponse(
            makeJsonDump(
                resultData=list(telecomNetworkCompany)
            ),
            content_type="application/json"
        )
    else:
        raise Http404()
