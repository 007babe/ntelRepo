from __future__ import absolute_import

import json

from django.db import transaction
from django.db.models.expressions import F
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, Http404
from django.shortcuts import render

from common.models import ComCd
from system.forms import SysCompanyForm
from system.models import SysAppreq, SysCompany, SysShop, SysUser
from utils.ajax import login_required_ajax
from utils.data import getSysSeqId
from utils.json import makeJsonResult, jsonDefault


@login_required_ajax
def appreqmanIndexCV(request):
    '''
    시스템관리 > 사용관리  : 이용신청관리 :  메인화면
    '''
    return render(
        request,
        'sysman/useman/appreqman/index.html',
        {},
    )

@login_required_ajax
def appreqmanDetailCV(request):
    '''
    시스템관리 > 사용관리  : 이용신청관리 :  상세
    '''
    if request.method == 'POST':
        qry = Q()
        qry &= Q(
            reqId__exact=request.POST.get("reqId")
        )
    else:
        raise Http404

    appreq = SysAppreq.objects.annotate(
        companyTpNm=F("companyTp__comNm")
    ).get(
        qry
    )

    return render(
        request,
        'sysman/useman/appreqman/detail.html',
        {
            "appreq": appreq
        },
    )


@login_required_ajax
def appreqmanJsonList(request):
    """
    시스템관리 > 사용관리  : 이용신청관리 : 리스트 데이터 Json
    """
    # sysMenu
    qry = Q()

    sysAppreq = SysAppreq.objects.filter(
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
                resultData=list(sysAppreq)
            ),
            default=jsonDefault
        ),
        content_type="application/json"
    )


@transaction.atomic
@login_required_ajax
def appreqmanJsonAppr(request):
    '''
    이용신청 승인처리
    '''
    if request.method == 'POST':
        statusGrpCd = "S0008"  # 진행상태 Group 코드
        reqId = request.POST.get("reqId")  # 요청ID
        reqStatus = request.POST.get("reqStatus")  # 처리상태단축코드

        print(reqId, reqStatus, statusGrpCd + reqStatus)

        if reqStatus == 'F':  # 승인처리일 경우
            ##################################
            # 1. 승인처리 대상 사용요청데이터를 획득
            ##################################
            appreq = SysAppreq.objects.get(
                reqId__exact=request.POST.get("reqId")
            )

            ##################################
            # 2. SysCompany에 데이터 등록
            ##################################
            companyId = getSysSeqId('SELLID')  # 회사ID 획득
            shopId = companyId + "01"  # 기본매장ID 획득
            print(companyId, shopId)

            sysCompany = SysCompany.objects.create(
                companyId=companyId,
                companyNm=appreq.companyNm,
                companyTp=appreq.companyTp,
                companyGrade=appreq.companyGrade,
                isReal=True,
                policyId=appreq.policyId,
                bizLicNo1=appreq.bizLicNo1,
                bizLicNo2=appreq.bizLicNo2,
                bizLicNo3=appreq.bizLicNo3,
                telNo1=appreq.telNo1,
                telNo2=appreq.telNo2,
                telNo3=appreq.telNo3,
                cellNo1=appreq.cellNo1,
                cellNo2=appreq.cellNo2,
                cellNo3=appreq.cellNo3,
                bizTp=appreq.bizTp,
                bizKind=appreq.bizKind,
                zipCd=appreq.zipCd,
                addr1=appreq.addr1,
                addr2=appreq.addr2,
                regId=SysUser.objects.get(userId__exact=request.user.userId),
                modId=SysUser.objects.get(userId__exact=request.user.userId),
            )
            #sysCompany.save()
            ##################################
            # 3. SysShop에 데이터 등록
            ##################################
            sysShop = SysShop.objects.create(
                shopId=shopId,
                shopNm=appreq.shopNm,
                companyId=sysCompany,
                telNo1=appreq.telNo1,
                telNo2=appreq.telNo2,
                telNo3=appreq.telNo3,
                cellNo1=appreq.cellNo1,
                cellNo2=appreq.cellNo2,
                cellNo3=appreq.cellNo3,
                zipCd=appreq.zipCd,
                addr1=appreq.addr1,
                addr2=appreq.addr2,
                regId=SysUser.objects.get(userId__exact=request.user.userId),
                modId=SysUser.objects.get(userId__exact=request.user.userId),
            )
            #sysShop.save()
            ##################################
            # 5. SysUser에 데이터 등록
            ##################################
            sysUser = SysUser.objects.create(
                userId=appreq.userId,
                password=appreq.password,
                email=appreq.email,
                userNm=appreq.userNm,
                userAuth=ComCd.objects.get(comCd__exact="S0001C"),
                shopId=sysShop,
                telNo1=appreq.telNo1,
                telNo2=appreq.telNo2,
                telNo3=appreq.telNo3,
                cellNo1=appreq.cellNo1,
                cellNo2=appreq.cellNo2,
                cellNo3=appreq.cellNo3,
                zipCd=appreq.zipCd,
                addr1=appreq.addr1,
                addr2=appreq.addr2,
                regId=SysUser.objects.get(userId__exact=request.user.userId),
                modId=SysUser.objects.get(userId__exact=request.user.userId),
            )
            #sysUser.save()

            ##################################
            # 6. 진행상태 Update
            ##################################
            appreq.reqStatus_id = statusGrpCd + reqStatus  # 요청상태 업데이트
            appreq.companyId = sysCompany
            appreq.save()

        elif reqStatus == 'C':  # 승인취소일 경우
            pass
    else:
        raise Http404

    return HttpResponse(
        json.dumps(
            makeJsonResult()
        ),
        content_type="application/json"
    )


@login_required_ajax
def companymanIndexCV(request):
    '''
    시스템관리 > 사용관리  : 사용회사관리 컨텐츠
    '''
    return render(
        request,
        'sysman/useman/companyman/index.html',
        {},
    )


@login_required_ajax
def usermanIndexCV(request):
    '''
    시스템관리 > 사용관리  : 사용자관리 컨텐츠
    '''
    return render(
        request,
        'sysman/useman/userman/index.html',
        {},
    )
