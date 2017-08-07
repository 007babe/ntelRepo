from __future__ import absolute_import

import json

from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.decorators.csrf import csrf_exempt

from utils.json import makeJsonResult


@csrf_exempt
def loginCV(request):
    '''
    로그인 화면 Contents View(Function Based)
    '''
    # 이미 로그인이 되었을 경우 메인 화면으로 이동한다
    if request.user.is_authenticated:
        return HttpResponseRedirect('/main')

    # 템플릿 렌더링 및 데이터 전달
    return render(
        request,
        'logins/login.html',
        {}
    )


def loginPopCV(request):
    '''
    로그인 팝업 화면 Contents View(Function Based)
    '''
    # 템플릿 렌더링 및 데이터 전달
    return render(
        request,
        'logins/loginpop.html',
        {}
    )


def loginCheckCV(request):
    '''
    로그인 화면 Contents View(Function Based)
    '''
    jsonResult = {}
    if request.method == 'POST':
        # 사용자 체크
        user = authenticate(
            request,
            userId=request.POST.get('userId'),
            password=request.POST.get('password')
        )

        # 추가 필요 : 업체, 매장, UseYn... authenticate 관련
        if user is not None:
            # Login 처리
            login(request, user)
            jsonResult = makeJsonResult(
                resultMessage="정상사용자"
            )
        else:
            jsonResult = makeJsonResult(
                False,
                resultMessage="비밀번호가 일치하지 않거나 사용이 불가한 사용자입니다."
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


def logoutCV(request):
    '''
    로그아웃 화면 Contents View(Function Based)
    '''
    # 로그아웃 처리
    logout(request)

    # 로그인 화면으로 이동
    return HttpResponseRedirect(reverse("logins:login"))
