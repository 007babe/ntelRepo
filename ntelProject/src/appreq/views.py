from __future__ import absolute_import

import json
from smtplib import SMTPDataError

from django.core.mail import send_mail
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, Http404
from django.shortcuts import render
from django.template.context_processors import request

from appreq.forms import SysAppReqForm
from system.models import SysAppReq
from system.models import SysPolicy
from utils.ajax import login_required_ajax
from utils.data import getComCdList
from utils.data import isUsableId
from utils.json import makeJsonResult


def appReqCV(request):
    '''
    이용신청 초기 화면 Contents View(Function Based)
    '''
    # 운영정책, 개인보호 정책 데이터 획득
    qry = Q()  # 쿼리조건
    qry &= Q(useYn__exact=True)  # 사용여부

    sysPolicy = SysPolicy.objects.filter(
        qry
    ).order_by(
        '-id'
    ).first()

    # 업체구분 데이터 획득
    companyTps = getComCdList(grpCd='S0004', grpOpt='B')

    # 템플릿 렌더링 및 데이터 전달
    return render(
        request,
        'appreq/index.html',
        {
            "sysPolicy": sysPolicy,
            "companyTps": companyTps,
        },
    )


def appReqResultPopCV(request):
    '''
    이용신청 결과 처리 Popup
    '''
    if request.POST:
        qry = Q()
        qry &= Q(reqId__exact=request.POST.get("reqId"))
        appreq = SysAppReq.objects.get(
            qry
        )

        # 템플릿 렌더링 및 데이터 전달
        return render(
            request,
            'appreq/result_pop.html',
            {"appreq": appreq},
        )
    else:
        raise Http404


def appReqRegistSV(request):
    '''
    이용신청 요청처리
    '''
    resultData = {}

    if request.method == 'POST':
        # 이용신청 폼
        sysAppReqForm = SysAppReqForm(
            request.POST,
        )

        # 데이터 검증 후 저장
        if(sysAppReqForm.is_valid()):
            sysAppReqForm.save()
            resultData["reqId"] = sysAppReqForm.reqId

            # 가입후 메일 보내기(함수, 클래스 화 => 쓰레드 처리) ===>
            try:
                print("sendmail -------------->")
                send_mail(
                    '엔텔에 가입해 주셔서 감사합니다.',
                    '엔텔 ',
                    'ntel5004@naver.com',
                    [sysAppReqForm.cleaned_data.get("email")],
                    fail_silently=False,
                )
                print(sysAppReqForm.cleaned_data.get("email"))
                print("sendmail --------------<")
            except SMTPDataError as smtpErr:
                print("메일 발송 실패")
                print(smtpErr)
            # 가입후 메일 보내기(함수, 클래스 화 => 쓰레드 처리) ===<

    return HttpResponse(
        json.dumps(
            makeJsonResult(
                form=sysAppReqForm,
                resultData=resultData
            )
        ),
        content_type="application/json"
    )


def getJsonIsUsableId(request):
    '''
    아이디 중복 체크 Contents View(Function Based)
    '''
    jsonResult = {}
    if request.method == 'POST':
        if isUsableId(request.POST.get("userId")):
            jsonResult = makeJsonResult(
                resultMessage="이용가능한 아이디입니다."
            )
        else:
            jsonResult = makeJsonResult(
                False,
                resultMessage="사용하실 수 없는 아이디입니다"
            )
    else:
        jsonResult = makeJsonResult(
            False,
            resultMessage="접근거부"
        )

    return HttpResponse(
        json.dumps(jsonResult),
        content_type="application/json"
    )


@login_required_ajax
def getJsonAppReq(request):
    '''
    이용신청 리스트 데이터 조회
    '''
    # 검색조건
    qry = Q()
    appReqs = SysAppReq.objects.filter(
        qry
    ).order_by(
        '-reqDt'
    )

    return HttpResponse(
        json.dumps(
            makeJsonResult(
                resultData=appReqs
            )
        ),
        content_type="application/json"
    )
