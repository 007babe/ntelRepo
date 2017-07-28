"""ntelProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.common/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from config import settings


urlpatterns = [
    # Admin Url
    url(r'^admin/', admin.site.urls),

    # 인증 및 권한관련(로그인, 비밀번호 변경, 회원가입...)
#    url(r'^accounts/', include('django.contrib.auth.urls',)), # 장고 내장 Auth
    
    #  시스템일반 서비스 URL 설정    
    url(r'', include('home.urls', namespace='home',),), # / Home
    url(r'^common/', include('common.urls', namespace='common',),), # /common 연결
    url(r'^system/', include('system.urls', namespace='system',),), # /system 연결
    url(r'^logins/', include('logins.urls', namespace='logins',),), # /logins 연결 : 로그인관련
    url(r'^appreq/', include('appreq.urls', namespace='appreq',),), # /appreq 연결 : 이용신청
    url(r'^main/', include('main.urls', namespace='main',),), # /main 연결 : 메인화면
    url(r'^open/', include('open.urls', namespace='open',),), # /open 연결 : 개통업무
    url(r'^plan/', include('plan.urls', namespace='plan',),), # /plan 연결 : 미결업무
    url(r'^reserve/', include('reserve.urls', namespace='reserve',),), # /reserve 연결 : 예약업무
    url(r'^custman/', include('custman.urls', namespace='custman',),), # /custman 연결 : 고객관리
    url(r'^receipt/', include('receipt.urls', namespace='receipt',),), # /receipt 연결 : 수납/장부
    url(r'^report/', include('report.urls', namespace='report',),), # /report 연결 : 통계리포트
    url(r'^setting/', include('setting.urls', namespace='setting',),), # /setting 연결 : 환경설정
    
    # 시스템관리 서비스 URL 설정
    url(r'^sysman/', include('sysman.urls', namespace='sysman',),), # /sysman 연결 : 시스템관리
    
    # Sample용
#    url(r'^bookmark/', include('bookmark.urls', namespace='bookmark',),), # /bookmark 연결
#    url(r'^blog/', include('blog.urls', namespace='blog',),), # /blog 연결
    url(r'^sample/', include('sample.urls', namespace='sample',),), # /sample 연결


]
