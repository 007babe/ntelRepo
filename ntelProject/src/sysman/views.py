from __future__ import absolute_import

import json

from django.core import serializers
from django.db.models.expressions import F, Value
from django.db.models.functions.base import Concat
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import render

from system.models import SysMenu, SysAppReq
from utils.ajax import login_required_ajax
from utils.json import makeJsonResult, jsonDefault


@login_required_ajax
def useAppReqCV(request):
    '''
    시스템관리 > 사용관리  : 이용신청관리 컨텐츠
    '''
    return render(
        request,
        'sysman/use/app_req.html',
        {},
    )

@login_required_ajax
def useAppReqDetailCV(request):
    '''
    시스템관리 > 사용관리  : 이용신청관리 컨텐츠 상세
    '''
    qry = Q()
    qry &= Q(
        reqId__exact=request.POST.get("reqId")
    )

    appReq = SysAppReq.objects.get(
        qry
    )

    return render(
        request,
        'sysman/use/app_req_detail.html',
        {
            "appReq": appReq
        },
    )


@login_required_ajax
def useAppReqListJson(request):
    """
    시스템관리 > 사용관리  : 이용신청관리 Json List
    """
    # sysMenu
    qry = Q()

    sysAppReq = SysAppReq.objects.filter(
        qry
    ).order_by(
        '-modDt',
    ).annotate(
        companyTpNm=F('companyTp__comNm'),
        companyGradeNm=F('companyGrade__comNm'),
#        telNo=Concat(Concat('telNo1',  Value('-'), 'telNo2'), Value('-'), 'telNo3'),
#        cellNo=Concat(Concat('cellNo1',  Value('-'), 'cellNo2'), Value('-'), 'cellNo3'),
        reqStatusNm=F('reqStatus__comNm'),
        reqStatusCss=F('reqStatus__cdCss'),
        regNm=F('regId__userNm'),
        modNm=F('modId__userNm'),
    ).values(
        "reqId",
        "reqDt",
        "companyNm",
        "companyTpNm",
        "companyGradeNm",
        "shopNm",
        "addr1",
        "useYn",
        "telNo1",
        "telNo2",
        "telNo3",
        "cellNo1",
        "cellNo2",
        "cellNo3",
        "regNm",
        "userId",
        "userNm",
        "email",
        "reqStatus",
        "reqStatusNm",
        "reqStatusCss",
    )

    return HttpResponse(
        json.dumps(
            makeJsonResult(
                resultData=list(sysAppReq)
            ),
            default=jsonDefault
        ),
        content_type="application/json"
    )


@login_required_ajax
def useCompanyCV(request):
    '''
    시스템관리 > 사용관리  : 사용회사관리 컨텐츠
    '''
    return render(
        request,
        'sysman/use/company.html',
        {},
    )


@login_required_ajax
def useUserCV(request):
    '''
    시스템관리 > 사용관리  : 사용자관리 컨텐츠
    '''
    return render(
        request,
        'sysman/use/user.html',
        {},
    )
