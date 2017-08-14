from __future__ import absolute_import

import json

from django.db.models.expressions import F
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, Http404
from django.shortcuts import render

from system.models import SysUser
from utils.ajax import login_required_ajax
from utils.date import getltdt
from utils.json import makeJsonResult, jsonDefault


@login_required_ajax
def staffmanJsonList(request):
    """
    환경설정 > 직원관리  : 리스트 데이터 Json
    """
    if request.method == 'POST' and request.user.userAuth_id in ["S0001M", "S0001C", "S0001A"]:
        userAuth = request.user.userAuth_id  # 사용자 권한 코드

        # Query
        qry = Q()
        # 동일회사조건
        qry &= Q(shopId__companyId__exact=request.user.shopId.companyId)
        # 총괄일 경우는 소속매장 직원만 조회
        if userAuth == "S0001A":
            qry &= Q(shopId__exact=request.user.shopId)

        # 검색조건
        qry &= Q(userNm__contains=request.POST.get("sUserNm"))  # 직원명
        qry &= Q(userId__contains=request.POST.get("sUserId"))  # 직원아이디
        qry &= Q(userAuth__comCd__contains=request.POST.get("sUserAuth"))  # 직원아이디

        # Exclude Query
        qryEx = Q()

        if userAuth not in ["S0001M", "S0001C"]:
            qryEx &= Q(userAuth__in=["S0001M", "S0001C"])

        staffs = SysUser.objects.filter(
            qry
        ).exclude(
            qryEx
        ).annotate(
            shopNm=F('shopId__shopNm'),  # 매장명
            companyNm=F('shopId__companyId__companyNm'),  # 회사명
            userAuthNm=F('userAuth__comNm'),  # 권한명
            regNm=F('regId__userNm'),  # 등록자명
            modNm=F('modId__userNm'),  # 수정자명
            lastLogin=F('last_login'),  # 마지막 로그인 일시
            authSeq=F('userAuth__ordSeq'),  # 권한정렬순서
        ).order_by(
            "shopId",
            "authSeq",
            "userNm",
        ).values(
            "useYn",
            "shopNm",
            "userAuth",
            "userAuthNm",
            "userNm",
            "userId",
            "telNo1",
            "telNo2",
            "telNo3",
            "cellNo1",
            "cellNo2",
            "cellNo3",
            "addr1",
            "lastLogin",
            "regDt",
            "companyNm",
            "email",
            "authSeq",
        )

        return HttpResponse(
            json.dumps(
                makeJsonResult(
                    resultData=list(staffs)
                ),
                default=jsonDefault
            ),
            content_type="application/json"
        )
    else:
        raise Http404


@login_required_ajax
def staffmanDetailCV(request):
    '''
    환경설정 > 직원관리 : 상세
    '''
    if request.method == 'POST' and request.user.userAuth_id in ["S0001M", "S0001C", "S0001A"]:
        # Query
        qry = Q()
        # 동일회사조건
        qry &= Q(shopId__companyId__exact=request.user.shopId.companyId)
        # 총괄일 경우는 소속매장 직원만 가능
        if request.user.userAuth not in ["S0001A"]:
            qry &= Q(shopId__exact=request.user.shopId)

        qry &= Q(
            userId__exact=request.POST.get("userId")
        )

        userInfo = SysUser.objects.annotate(
            companyNm=F("shopId__companyId__companyNm"),
            shopNm=F("shopId__shopNm"),
        ).get(
            qry
        )

        return render(
            request,
            'setting/staffman/detail.html',
            {
                "userInfo": userInfo
            },
        )
    else:
        raise Http404
