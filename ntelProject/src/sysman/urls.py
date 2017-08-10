from django.conf.urls import url

from . import views


urlpatterns = [
    #===============================>
    # 사용관리(submenu)
    #===============================<
    ########################
    # 이용신청관리(tab)
    ########################
    # 이용신청관리 화면
    url(r'^useman/appreqman/$', views.appreqmanIndexCV, name='useman__appreqman'),
    # 이용신청관리 리스트(Json)
    url(r'^useman/appreqman/json/list/$', views.appreqmanJsonList, name='useman__appreqman__json__list'),
    # 이용신청관리 승인/취소 처리(Json)
    url(r'^useman/appreqman/json/appr$', views.appreqmanDetailCV, name='useman__appreqman__json_appr'),

    # 이용신청관리 상세 화면
    url(r'^useman/appreqman/detail/$', views.appreqmanDetailCV, name='useman__appreqman__detail'),

    ########################
    # 사용회사관리(tab)
    ########################
    # 사용회사관리 화면
    url(r'^useman/companyman/$', views.companymanIndexCV, name='useman__companyman'),

    ########################
    # 사용자관리(tab)
    ########################
    # 사용자관리화면
    url(r'^useman/userman/$', views.usermanIndexCV, name='useman__userman'),

    #===============================>
    # 메뉴관리(submenu)
    #===============================<
    # url(r'^menu/tab1/$', views.sysmanMenuTab1CV, name='menu_tab1',),
]
