from __future__ import absolute_import

import json

from django.core.exceptions import PermissionDenied
from django.db.models.expressions import F
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, Http404
from django.shortcuts import render

from system.models import SysUser
from utils.ajax import login_required_ajax, login_required_ajax_post
from utils.data import is_empty
from utils.date import getltdt
from utils.json import makeJsonResult, jsonDefault


@login_required_ajax_post
def staffmanJsonList(request):
    """
    환경설정 > 직원관리  : 리스트 데이터 Json
    """
    userAuth = request.user.userAuth_id  # 사용자 권한 코드

    # 검색조건
    sShopId = request.POST.get("sShopId")
    sUserNm = request.POST.get("sUserNm")
    sUserId = request.POST.get("sUserId")
    sUserAuth = request.POST.get("sUserAuth")

    if userAuth in ["S0001M", "S0001C", "S0001A", "S0001T"]:  # 시스템관리자, 대표, 총괄, 점장만 가능
        # Query
        qry = Q()
        ####################
        # 기본 조건
        ####################
        # 동일회사조건
        qry &= Q(shopId__companyId__exact=request.user.shopId.companyId)

        # 팀장일 경우는 소속매장 직원만 조회
        if userAuth == "S0001T":
            qry &= Q(shopId__exact=request.user.shopId)

        ####################
        # 검색 조건
        ####################
        if not is_empty(sShopId):  # 검색 매장아이디가 있을 경우
            qry &= Q(shopId__exact=sShopId)
        qry &= Q(userNm__contains=sUserNm)  # 직원명
        qry &= Q(userId__contains=sUserId)  # 직원아이디
        qry &= Q(userAuth__comCd__contains=sUserAuth)  # 직원권한

        ####################
        # 제외 조건
        ####################
        # Exclude Query
        qryEx = Q()

        if userAuth not in ["S0001M", "S0001C", "S0001A"]:  # 시스템관리자, 대표, 총괄이 아닐 경우 팀장 이하만 조회
            qryEx &= Q(userAuth__in=["S0001M", "S0001C", "S0001A"])
        elif userAuth not in ["S0001M", "S0001C"]:  # 시스템관리자, 대표가 아닐 경우 총괄 이하만 조회
            qryEx &= Q(userAuth__in=["S0001M", "S0001C"])
        elif userAuth not in ["S0001M"]:  # 시스템관리자 아닐 경우 대표 이하만 조회
            qryEx &= Q(userAuth__in=["S0001M"])

        ####################
        # 조회
        ####################
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
        raise PermissionDenied()


@login_required_ajax_post
def staffmanDetailCV(request):
    '''
    환경설정 > 직원관리 : 상세
    '''
    userAuth = request.user.userAuth_id  # 사용자 권한 코드

    if userAuth in ["S0001M", "S0001C", "S0001A", "S0001T"]:  # 시스템관리자, 대표, 총괄, 점장만 가능

        # Query
        qry = Q()
        ####################
        # 기본 조건
        ####################
        # 동일회사조건
        qry &= Q(shopId__companyId__exact=request.user.shopId.companyId)
        # 점장일 경우는 소속매장 직원만 가능
        if request.user.userAuth not in ["S0001A"]:
            qry &= Q(shopId__exact=request.user.shopId)
        # 해당 사용자 ID
        qry &= Q(
            userId__exact=request.POST.get("userId")
        )

        ####################
        # 조회
        ####################
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
        raise PermissionDenied()
