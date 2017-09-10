from __future__ import absolute_import

import json
import pprint

from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.db import connection, transaction
from django.db.models.aggregates import Count
from django.db.models.expressions import F, Subquery, Case, When
from django.db.models.fields import CharField, IntegerField
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, Http404
from django.middleware import csrf
from django.shortcuts import render

from setting.forms import StaffModifyForm, StaffRegistForm, ShopModifyForm, \
    ShopRegistForm, CompanyAccountRegistForm, \
    AccountRegistForm, AccountModifyForm
from system.models import SysUser, SysShop, SysCompanyAccount, SysCompany, \
    SysComCd
from utils.ajax import login_required_ajax_post
from utils.data import is_empty, getComCdList, dictfetchall, getSysShopId, \
    getNetworkCompanyByNetworkGroupList
from utils.date import getltdt
from utils.json import makeJsonResult, jsonDefault, JSONSerializer


@login_required_ajax_post
def staffmanRegistCV(request):
    '''
    환경설정 > 직원관리 : 직원등록
    '''
    userAuth = request.user.userAuth_id  # 사용자 권한 코드

    if userAuth in ["S0001M", "S0001C", "S0001A", "S0001T"]:  # 시스템관리자, 대표, 총괄, 점장만 가능
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

        return render(
            request,
            'setting/staffman/regist.html',
            {
                "userAuths": userAuths,
                "userShops": userShops,
            },
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
        # 해당 사용자 ID
        qry &= Q(
            userId__exact=request.POST.get("userId")
        )

        ####################
        # 조회
        ####################
        # 직원 정보 데이터 획득
        staffInfo = None
        if userAuth == "S0001T":  # 점장일 경우
            staffInfo = SysUser.objects.for_shop(request.user.shopId)
        else:
            staffInfo = SysUser.objects.for_company(request.user.shopId.companyId)

        staffInfo = staffInfo.get(
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
def staffmanJsonList(request):
    '''
    환경설정 > 직원관리  : 리스트 데이터 Json
    '''
    userAuth = request.user.userAuth_id  # 사용자 권한 코드

    # 시스템관리자, 대표, 총괄, 점장만 가능
    if userAuth in ["S0001M", "S0001C", "S0001A", "S0001T"]:
        # 검색조건(Parameter)
        sUseYn = request.POST.get("sUseYn")
        sShopId = request.POST.get("sShopId")
        sUserNm = request.POST.get("sUserNm")
        sUserId = request.POST.get("sUserId")
        sUserAuth = request.POST.get("sUserAuth")

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
        if userAuth == "S0001T":  # 점장일 경우
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
def staffmanJsonModify(request):
    '''
    직원정보 수정 요청처리
    '''
    userAuth = request.user.userAuth_id  # 사용자 권한 코드

    if userAuth in ["S0001M", "S0001C", "S0001A", "S0001T"]:  # 시스템관리자, 대표, 총괄, 점장만 가능
        resultData = {}

        # 수정할 데이터 획득
        staffInfo = SysUser.objects.for_company(request.user.shopId.companyId).get(
            userId=request.POST.get("userId")
        )

        # 직원정보 수정 폼
        staffModifyForm = StaffModifyForm(
            request.POST,
            instance=staffInfo,
            request=request,
        )

        # 데이터 검증 후 저장
        if staffModifyForm.is_valid():
            staffModifyForm.save()

        return HttpResponse(
            json.dumps(
                makeJsonResult(
                    form=staffModifyForm,
                    resultMessage="수정되었습니다.",
                    resultData=resultData
                )
            ),
            content_type="application/json"
        )
    else:
        raise PermissionDenied()


@login_required_ajax_post
def staffmanJsonRegist(request):
    '''
    직원정보 등록 요청처리
    '''
    userAuth = request.user.userAuth_id  # 사용자 권한 코드

    if userAuth in ["S0001M", "S0001C", "S0001A", "S0001T"]:  # 시스템관리자, 대표, 총괄, 점장만 가능
        resultData = {}

        # 직원정보 등록 폼
        staffRegistForm = StaffRegistForm(
            request.POST,
            request=request,
        )

        # 데이터 검증 후 저장
        if staffRegistForm.is_valid():
            staffRegistForm.save()

        return HttpResponse(
            json.dumps(
                makeJsonResult(
                    form=staffRegistForm,
                    resultMessage="등록되었습니다.",
                    resultData=resultData
                )
            ),
            content_type="application/json"
        )
    else:
        raise PermissionDenied()


@login_required_ajax_post
def shopmanRegistCV(request):
    '''
    환경설정 > 직원관리 : 직원등록
    '''
    userAuth = request.user.userAuth_id  # 사용자 권한 코드

    if userAuth in ["S0001M", "S0001C", "S0001A"]:  # 시스템관리자, 대표, 총괄만 가능

        return render(
            request,
            'setting/shopman/regist.html',
            {},
        )
    else:
        raise PermissionDenied()  # 403에러


@login_required_ajax_post
def shopmanDetailCV(request):
    '''
    환경설정 > 매장관리 : 상세
    '''
    userAuth = request.user.userAuth_id  # 사용자 권한 코드

    if userAuth in ["S0001M", "S0001C", "S0001A"]:  # 시스템관리자, 대표, 총괄만 가능
        # Query
        qry = Q()
        ####################
        # 기본 조건
        ####################
        # 해당 사용자 ID
        qry &= Q(
            shopId__exact=request.POST.get("shopId")
        )

        ####################
        # 조회
        ####################
        # 직원 정보 데이터 획득
        shopInfo = SysShop.objects.for_company(
            request.user.shopId.companyId
        ).get(
            qry
        )

        # Rendering
        return render(
            request,
            'setting/shopman/detail.html',
            {
                "shopInfo": shopInfo,
            },
        )
    else:
        raise PermissionDenied()


@login_required_ajax_post
def shopmanJsonList(request):
    '''
    환경설정 > 매장관리  : 리스트 데이터 Json
    '''
    userAuth = request.user.userAuth_id  # 사용자 권한 코드

    if userAuth in ["S0001M", "S0001C", "S0001A"]:  # 시스템관리자, 대표, 총괄만 가능
        # 검색조건(Parameter)
        sUseYn = request.POST.get("sUseYn")
        sShopNm = request.POST.get("sShopNm")

        # Query
        qry = Q()
        ####################
        # 검색 조건
        ####################
        if not is_empty(sUseYn):  # 사용여부
            qry &= Q(useYn__exact=sUseYn)

        qry &= Q(shopNm__contains=sShopNm)  # 매장명

        shopInfos = SysShop.objects.for_company(request.user.shopId.companyId)

        shopInfos = shopInfos.filter(
            qry
        ).annotate(
            staffCnt=Count("r_system_sysuser_shop_id"),
            staffCntUseY=Count(
                Case(
                    When(r_system_sysuser_shop_id__useYn__exact=True, then=1),
                    output_field=IntegerField(),
                )
            ),
            staffCntUseN=Count(
                Case(
                    When(r_system_sysuser_shop_id__useYn__exact=False, then=1),
                    output_field=IntegerField(),
                )
            )
        ).order_by(
            "-useYn",
        ).values(
            "shopId",
            "shopNm",
            "zipCd",
            "addr1",
            "addr2",
            "useYn",
            "cellNo1",
            "cellNo2",
            "cellNo3",
            "telNo1",
            "telNo2",
            "telNo3",
            "faxNo1",
            "faxNo2",
            "faxNo3",
            "isMain",
            "staffCnt",
            "staffCntUseY",
            "staffCntUseN",
            "regDt",
            "regId",
            "modDt",
            "modId",
        )

        return HttpResponse(
            json.dumps(
                makeJsonResult(
                    resultData=list(shopInfos)
                ),
                default=jsonDefault
            ),
            content_type="application/json"
        )
    else:
        raise PermissionDenied()


@login_required_ajax_post
def shopmanJsonModify(request):
    '''
    매장정보 수정 요청처리
    '''
    userAuth = request.user.userAuth_id  # 사용자 권한 코드

    if userAuth in ["S0001M", "S0001C", "S0001A"]:  # 시스템관리자, 대표, 총괄만 가능
        resultData = {}

        # 수정할 데이터 획득
        shopInfo = SysShop.objects.for_company(request.user.shopId.companyId).get(
            shopId=request.POST.get("shopId")
        )

        # 매장정보 수정 폼
        shopModifyForm = ShopModifyForm(
            request.POST,
            instance=shopInfo,
            request=request,
        )

        # 데이터 검증 후 저장
        if shopModifyForm.is_valid():
            shopModifyForm.save()

        return HttpResponse(
            json.dumps(
                makeJsonResult(
                    form=shopModifyForm,
                    resultMessage="수정되었습니다.",
                    resultData=resultData
                )
            ),
            content_type="application/json"
        )
    else:
        raise PermissionDenied()


@login_required_ajax_post
def shopmanJsonRegist(request):
    '''
    직원정보 등록 요청처리
    '''
    userAuth = request.user.userAuth_id  # 사용자 권한 코드

    if userAuth in ["S0001M", "S0001C", "S0001A"]:  # 시스템관리자, 대표, 총괄만 가능
        resultData = {}

        # 매장정보 등록 폼
        shopRegistForm = ShopRegistForm(
            request.POST,
            request=request,
        )

        # 데이터 검증 후 저장
        if shopRegistForm.is_valid():
            shopRegistForm.save()

        return HttpResponse(
            json.dumps(
                makeJsonResult(
                    form=shopRegistForm,
                    resultMessage="등록되었습니다.",
                    resultData=resultData
                )
            ),
            content_type="application/json"
        )
    else:
        raise PermissionDenied()



@login_required_ajax_post
def accountmanRegistCV(request):
    '''
    환경설정 > 직원관리 : 직원등록
    '''
    userAuth = request.user.userAuth_id  # 사용자 권한 코드

    if userAuth in ["S0001M", "S0001C", "S0001A"]:  # 시스템관리자, 대표, 총괄만 가능

        # 거래처(회사) 구분값 획득(공통코드)
        companyTps = SysComCd.objects.for_grp(
            grpCd="S0004",
            grpOpt="B",
        ).exclude(
            comCd__exact=request.user.shopId.companyId.companyTp
        )

        # 망별 통신사 코드 데이터 획득
        networkCompanys = getNetworkCompanyByNetworkGroupList()

        return render(
            request,
            'setting/accountman/regist.html',
            {
                "companyTps": companyTps,
                "networkCompanys": networkCompanys,
            },
        )
    else:
        raise PermissionDenied()  # 403에러


@login_required_ajax_post
def accountmanDetailCV(request):
    '''
    환경설정 > 거래처관리 : 상세
    '''
    userAuth = request.user.userAuth_id  # 사용자 권한 코드

    if userAuth in ["S0001M", "S0001C", "S0001A"]:  # 시스템관리자, 대표, 총괄만 가능
        # Query
        qry = Q()
        ####################
        # 기본 조건
        ####################
        # 해당 사용자 ID
        qry &= Q(
            id__exact=request.POST.get("id")
        )

        ####################
        # 조회
        ####################
        # 거래처 정보 데이터 획득
        accountInfo = SysCompanyAccount.objects.for_company(
            request.user.shopId.companyId
        ).get(
            qry
        )

        # 거래처(회사) 구분값 획득(공통코드)
        companyTps = SysComCd.objects.for_grp(
            grpCd="S0004",
            grpOpt="B",
        ).exclude(
            comCd__exact=request.user.shopId.companyId.companyTp
        )

        # 망별 통신사 코드 데이터 획득
        networkCompanys = getNetworkCompanyByNetworkGroupList()

        # 수정가능 여부 확인 후 세팅
        editable = True
        if accountInfo.accountId.isReal:  # 실매장일 경우 수정불가
            editable = False

        # Rendering
        return render(
            request,
            'setting/accountman/detail.html',
            {
                "accountInfo": accountInfo,
                "networkCompanys": networkCompanys,
                "editable": editable,
            },
        )
    else:
        raise PermissionDenied()


@login_required_ajax_post
def accountmanJsonList(request):
    '''
    환경설정 >  거래처관리  : 리스트 데이터 Json
    '''
    userAuth = request.user.userAuth_id  # 사용자 권한 코드

    if userAuth in ["S0001M", "S0001C", "S0001A"]:  # 시스템관리자, 대표, 총괄만 가능
        # 검색조건(Parameter)
        sUseYn = request.POST.get("sUseYn")
        sCompanyTp = request.POST.get("sCompanyTp")
        sAccountNm = request.POST.get("sAccountNm")

        # Query
        qry = Q()
        ####################
        # 검색 조건
        ####################
        if not is_empty(sUseYn):  # 사용여부
            qry &= Q(useYn__exact=sUseYn)

        qry &= Q(accountId__companyTp__comCd__contains=sCompanyTp)  # 거래처구분
        qry &= Q(accountId__companyNm__contains=sAccountNm)  # 거래처명

        accountInfos = SysCompanyAccount.objects.for_company(request.user.shopId.companyId)

        accountInfos = accountInfos.filter(
            qry
        ).annotate(
            accountNm=F('accountId__companyNm'),  # 거래처명
            companyTp=F('accountId__companyTp'),  # 거래처구분
            companyTpNm=F('accountId__companyTp__comNm'),  # 거래처구분명
            telNo1=F('accountId__telNo1'),  # 거래처전화1
            telNo2=F('accountId__telNo2'),  # 거래처전화2
            telNo3=F('accountId__telNo3'),  # 거래처전화3
            faxNo1=F('accountId__faxNo1'),  # 거래처Fax1
            faxNo2=F('accountId__faxNo2'),  # 거래처Fax2
            faxNo3=F('accountId__faxNo3'),  # 거래처Fax3
            cellNo1=F('accountId__cellNo1'),  # 거래처담당자휴대폰1
            cellNo2=F('accountId__cellNo2'),  # 거래처담당자휴대폰2
            cellNo3=F('accountId__cellNo3'),  # 거래처담당자휴대폰3
            addr1=F('accountId__addr1'),  # 거래처주소1
            addr2=F('accountId__addr2'),  # 거래처주소2
            isReal=F('accountId__isReal'),  # 시스템사용 실 거래처 여부
            networkCompanyId=F('accountId__networkCompanyId'),  # 망통신사
            chargerNm=F('accountId__chargerNm'),  # 담당자명
        ).order_by(
            "-useYn",
            "accountNm",
        ).values(
            "id",
            "companyId",
            "accountId",
            "accountNm",
            "companyTp",
            "companyTpNm",
            "addr1",
            "addr2",
            "useYn",
            "cellNo1",
            "cellNo2",
            "cellNo3",
            "telNo1",
            "telNo2",
            "telNo3",
            "faxNo1",
            "faxNo2",
            "faxNo3",
            "isReal",
            "networkCompanyId",
            "chargerNm",
            "regDt",
            "regId",
            "modDt",
            "modId",
        )

        return HttpResponse(
            json.dumps(
                makeJsonResult(
                    resultData=list(accountInfos)
                ),
                default=jsonDefault
            ),
            content_type="application/json"
        )
    else:
        raise PermissionDenied()


@login_required_ajax_post
def accountmanJsonModify(request):
    '''
    거래처정보 수정 요청처리
    '''
    userAuth = request.user.userAuth_id  # 사용자 권한 코드

    if userAuth in ["S0001M", "S0001C", "S0001A",]:  # 시스템관리자, 대표, 총괄만 가능
        resultData = {}

        # 수정할 데이터 획득
        accountInfo = SysCompany.objects.for_account(
            companyId=request.user.shopId.companyId,
            isReal=False,  # 실제 매장은 수정대상이 아님
        ).get(
            companyId__exact=request.POST.get("accountId")
        )

        # 거래처정보 수정 폼
        accountModifyForm = AccountModifyForm(
            request.POST,
            instance=accountInfo,
            request=request,
        )

        # 데이터 검증 후 저장
        if accountModifyForm.is_valid():
            accountModifyForm.save()

            # 거래처 연결 사용여부 저장
            comapnyAccount = SysCompanyAccount.objects.for_company(
                request.user.shopId.companyId
            ).get(
                accountId=accountInfo.companyId,
            )
            comapnyAccount.useYn = not is_empty(request.POST.get("useYn"))
            comapnyAccount.modId = request.user
            comapnyAccount.save()

        return HttpResponse(
            json.dumps(
                makeJsonResult(
                    form=accountModifyForm,
                    resultMessage="수정되었습니다.",
                    resultData=resultData,
                )
            ),
            content_type="application/json"
        )
    else:
        raise PermissionDenied()


@login_required_ajax_post
@transaction.atomic
def accountmanJsonRegist(request):
    '''
    거래처정보 등록 요청처리
    '''
    userAuth = request.user.userAuth_id  # 사용자 권한 코드

    if userAuth in ["S0001M", "S0001C", "S0001A"]:  # 시스템관리자, 대표, 총괄만 가능

        resultData = {}

        # 거래처정보 등록 폼
        accountRegistForm = AccountRegistForm(
            request.POST,
            request=request,
        )

        # 거래처 정보 등록
        if accountRegistForm.is_valid():
            # 거래처 회사 등록
            accountCompany = accountRegistForm.save()

            # 거래처 연결 등록
            SysCompanyAccount.objects.create(
                companyId=request.user.shopId.companyId,
                accountId=accountCompany,
                useYn=not is_empty(request.POST.get("useYn")),
                regId=request.user,
                modId=request.user,
            )

        return HttpResponse(
            json.dumps(
                makeJsonResult(
                    form=accountRegistForm,
                    resultMessage="등록되었습니다.",
                    resultData=resultData
                )
            ),
            content_type="application/json"
        )
    else:
        raise PermissionDenied()
