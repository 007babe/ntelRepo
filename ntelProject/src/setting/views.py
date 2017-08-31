from __future__ import absolute_import

import json

from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.db import connection
from django.db.models.expressions import F, Subquery
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, Http404
from django.middleware import csrf
from django.shortcuts import render

from common.models import ComCd
from setting.forms import StaffChangeForm
from system.models import SysUser, SysShop
from utils import data
from utils.ajax import login_required_ajax_post
from utils.data import is_empty, getComCdList, dictfetchall
from utils.date import getltdt
from utils.json import makeJsonResult, jsonDefault, JSONSerializer


@login_required_ajax_post
def staffmanJsonList(request):
    """
    환경설정 > 직원관리  : 리스트 데이터 Json
    """
    userAuth = request.user.userAuth_id  # 사용자 권한 코드

    # 검색조건
    sUseYn = request.POST.get("sUseYn")
    sShopId = request.POST.get("sShopId")
    sUserNm = request.POST.get("sUserNm")
    sUserId = request.POST.get("sUserId")
    sUserAuth = request.POST.get("sUserAuth")

    if userAuth in ["S0001M", "S0001C", "S0001A", "S0001T"]:  # 시스템관리자, 대표, 총괄, 점장만 가능
        # Query
        qry = Q()
        ####################
        # 검색 조건
        ####################
        if not is_empty(sUseYn):  # 사용여부
            qry &= Q(useYn__exact=sUseYn)

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
        staffInfos = None
        if userAuth == "S0001T":
            staffInfos = SysUser.objects.for_shop(request.user.shopId)
        else:
            staffInfos = SysUser.objects.for_company(request.user.shopId.companyId)

        staffInfos = staffInfos.filter(
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
            "-useYn",
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
            "connLimit",
            "loginCnt",
            "lastLogin",
            "regDt",
            "companyNm",
            "email",
            "authSeq",
        )

        return HttpResponse(
            json.dumps(
                makeJsonResult(
                    resultData=list(staffInfos)
                ),
                default=jsonDefault
            ),
            content_type="application/json"
        )
    else:
        raise PermissionDenied()


@login_required_ajax_post
def staffmanRegistCV(request):
    '''
    환경설정 > 직원관리 : 직원등록
    '''
    userAuth = request.user.userAuth_id  # 사용자 권한 코드
    if userAuth in ["S0001M", "S0001C", "S0001A", "S0001T"]:  # 시스템관리자, 대표, 총괄, 점장만 가능
        return render(
            request,
            'setting/staffman/regist.html',
            {},
        )
    else:
        raise PermissionDenied()  # 403에러


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
        # 동일회사조건(필수)
        qry &= Q(shopId__companyId__exact=request.user.shopId.companyId)

        # 점장일 경우는 소속매장 직원만 가능
        if userAuth in ["S0001T"]:
            qry &= Q(shopId__exact=request.user.shopId)

        # 해당 사용자 ID
        qry &= Q(
            userId__exact=request.POST.get("userId")
        )

        ####################
        # 조회
        ####################
        staffInfo = SysUser.objects.get(
            qry
        )

        # 권한리스트 데이터 획득
        userAuths = getComCdList(
            grpCd='S0001',
            grpOpt=request.user.userAuth.srtCd,
        ).filter(
            # 현재 사용자 권한에 따른 조건 처리(자신 포함 자신의 상위 권한 제외)
            ordSeq__gt=request.user.userAuth.ordSeq
        )

        # 매장리스트 데이터 획득
        qryShops = Q()
        qryShops &= Q(useYn__exact=True) 
        if userAuth in ["S0001M", "S0001C", "S0001A"]:
            qryShops &= Q(companyId__exact=request.user.shopId.companyId)
        else:
            qryShops &= Q(shopId__exact=request.user.shopId)

        userShops = SysShop.objects.filter(
            qryShops
        )

        # 수정가능 여부 확인 후 세팅
        editable = True
        if staffInfo.userId == request.user.userId or staffInfo.userAuth.ordSeq <= request.user.userAuth.ordSeq:
            editable = False

        # Rendering
        return render(
            request,
            'setting/staffman/detail.html',
            {
                "staffInfo": staffInfo,
                "userAuths": userAuths,
                "userShops": userShops,
                "editable": editable,
            },
        )
    else:
        raise PermissionDenied()


@login_required_ajax_post
def staffmanJsonModify(request):
    '''
    직원정보 수정 요청처리
    '''
    resultData = {}

    # 수정할 데이터 획득
    '''
    staffInfo = SysUser.objects.get(
        userId=request.POST.get("userId")
    )
    '''
    staffInfo = SysUser.objects.for_company(request.user.shopId.companyId).get(
        userId=request.POST.get("userId")
    )

    # 직원정보 수정 폼
    staffChangeForm = StaffChangeForm(
        request.POST,
        instance=staffInfo,
        request=request,
    )

    # 데이터 검증 후 저장
    if(staffChangeForm.is_valid()):
        staffChangeForm.save()

    return HttpResponse(
        json.dumps(
            makeJsonResult(
                form=staffChangeForm,
                resultMessage="수정되었습니다.",
                resultData=resultData
            )
        ),
        content_type="application/json"
    )
