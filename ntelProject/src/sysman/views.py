from __future__ import absolute_import

from datetime import datetime
import json

from django.db import transaction
from django.db.models.expressions import F
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, Http404
from django.shortcuts import render

from common.models import ComCd
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
    else:
        raise Http404


@login_required_ajax
def appreqmanJsonList(request):
    """
    시스템관리 > 사용관리  : 이용신청관리 : 리스트 데이터 Json
    """
    if request.method == 'POST':
        qry = Q()
        # 검색조건
        qry &= Q(reqStatus__comCd__contains=request.POST.get("sReqStatus"))  # 진행상태
        qry &= Q(reqId__contains=request.POST.get("sReqId"))  # 요청번호
        qry &= Q(companyNm__contains=request.POST.get("sCompanyNm"))  # 회사명
        qry &= Q(userNm__contains=request.POST.get("sUserNm"))  # 대표자명

        sysAppreq = SysAppreq.objects.annotate(
            companyTpNm=F('companyTp__comNm'),
            companyGradeNm=F('companyGrade__comNm'),
            reqStatusNm=F('reqStatus__comNm'),
            reqStatusCss=F('reqStatus__cdCss'),
            regNm=F('regId__userNm'),
            modNm=F('modId__userNm'),
        ).filter(
            qry
        ).order_by(
            '-reqId',
        ).values(
            "reqId",
            "reqDt",
            "appDt",
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
    else:
        raise Http404


@login_required_ajax
@transaction.atomic
def appreqmanJsonAppr(request):
    '''
    이용신청 승인처리
    '''
    if request.method == 'POST':
        statusGrpCd = "S0008"  # 진행상태 Group 코드
        reqId = request.POST.get("reqId")  # 요청ID
        reqStatus = request.POST.get("reqStatus")  # 진행상태단축코드

        ##################################
        # 0. 승인처리 대상 사용요청데이터를 획득
        ##################################
        appreq = SysAppreq.objects.get(
            reqId__exact=reqId
        )

        if reqStatus == 'F':  # 승인처리 요청일 경우

            ##################################
            # 1. SysCompany에 데이터 등록
            ##################################
            companyId = getSysSeqId('SELLID')  # 회사ID 획득
            shopId = companyId + "01"  # 기본매장ID 획득

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

            ##################################
            # 2. SysShop에 데이터 등록
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
                isMain=True,
                regId=SysUser.objects.get(userId__exact=request.user.userId),
                modId=SysUser.objects.get(userId__exact=request.user.userId),
            )

            ##################################
            # 3. SysUser에 데이터 등록
            ##################################
            SysUser.objects.create(
                userId=appreq.userId,
                password=appreq.password,
                useYn=True,
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

            ##################################
            # 4. 진행상태 Update => 승인처리(F)
            ##################################
            appreq.reqStatus_id = statusGrpCd + reqStatus  # 요청상태 업데이트
            appreq.appDt = datetime.now()
            appreq.companyId = sysCompany
            appreq.save()

        elif reqStatus == 'C':  # 요청취소일 경우
            ##################################
            # 1. 진행상태 Update => 요청취소(C)
            ##################################
            appreq.reqStatus_id = statusGrpCd + reqStatus  # 요청상태 업데이트
            appreq.appDt = datetime.now()
            appreq.save()
        elif reqStatus == 'A':  # 승인요청일 경우
            ##################################
            # 1. 진행상태 및 Update => 승인요청(A)
            ##################################
            appreq.reqStatus_id = statusGrpCd + reqStatus  # 요청상태 업데이트
            appreq.appDt = None
            appreq.save()
        elif reqStatus == 'D':  # 삭제일 경우
            sysCompany = SysCompany.objects.get(
                companyId__exact=appreq.companyId
            )
            sysCompany.delete()

        # 적용된 데이터를 다시 획득
        appreq = SysAppreq.objects.annotate(
            companyTpNm=F('companyTp__comNm'),
            companyGradeNm=F('companyGrade__comNm'),
            reqStatusNm=F('reqStatus__comNm'),
            reqStatusCss=F('reqStatus__cdCss'),
            regNm=F('regId__userNm'),
            modNm=F('modId__userNm'),
        ).filter(
            reqId__exact=reqId
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
        ).first()

        return HttpResponse(
            json.dumps(
                makeJsonResult(
                    resultMessage="처리가완료되었습니다.",
                    resultData=appreq,
                ),
                default=jsonDefault
            ),
            content_type="application/json"
        )

    else:
        raise Http404


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
