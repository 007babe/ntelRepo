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
    url(r'^use/app_req/$', views.useAppReqCV, name='use__app_req'),
    # 이용신청관리 리스트(Json)
    url(r'^use/app_req_man/list/json/$', views.useAppReqListJson, name='use__app_req__list__json'),
    # 이용신청관리 상세 화면
    url(r'^use/app_req_man/detail/$', views.useAppReqDetailCV, name='use__app_req__detail'),

    ########################
    # 사용회사관리(tab)
    ########################
    # 사용회사관리 화면
    url(r'^use/company/$', views.useCompanyCV, name='use__company'),

    ########################
    # 사용자관리(tab)
    ########################
    # 사용자관리화면
    url(r'^use/user/$', views.useUserCV, name='use__user'),

    #===============================>
    # 메뉴관리(submenu)
    #===============================<
    # url(r'^menu/tab1/$', views.sysmanMenuTab1CV, name='menu_tab1',),
]
