from django.conf.urls import url

from . import views


urlpatterns = [
    #===============================>
    # 거래처관리
    #===============================<
    # 거래처 리스트(Json)
    url(r'^accountman/json/list/$', views.accountmanJsonList, name='accountman__json__list'),
    # 거래처 정보 수정(Json)
    url(r'^accountman/json/modify/$', views.accountmanJsonModify, name='accountman__json__modify'),
    # 거래처 정보 등록(Json)
    url(r'^accountman/json/regist/$', views.accountmanJsonRegist, name='accountman__json__regist'),
    # 거래처 상세 화면
    url(r'^accountman/detail/$', views.accountmanDetailCV, name='accountman__detail'),
    # 거래처 등록 화면
    url(r'^accountman/regist/$', views.accountmanRegistCV, name='accountman__regist'),

    #===============================>
    # 직원관리
    #===============================<
    # 직원 리스트(Json)
    url(r'^staffman/json/list/$', views.staffmanJsonList, name='staffman__json__list'),
    # 직원 정보 수정(Json)
    url(r'^staffman/json/modify/$', views.staffmanJsonModify, name='staffman__json__modify'),
    # 직원 정보 등록(Json)
    url(r'^staffman/json/regist/$', views.staffmanJsonRegist, name='staffman__json__regist'),
    # 직원 상세 화면
    url(r'^staffman/detail/$', views.staffmanDetailCV, name='staffman__detail'),
    # 직원 등록 화면
    url(r'^staffman/regist/$', views.staffmanRegistCV, name='staffman__regist'),

    #===============================>
    # 매장관리
    #===============================<
    # 매장 리스트(Json)
    url(r'^shopman/json/list/$', views.shopmanJsonList, name='shopman__json__list'),
    # 매장 정보 수정(Json)
    url(r'^shopman/json/modify/$', views.shopmanJsonModify, name='shopman__json__modify'),
    # 매장 정보 등록(Json)
    url(r'^shopman/json/regist/$', views.shopmanJsonRegist, name='shopman__json__regist'),
    # 매장 상세 화면
    url(r'^shopman/detail/$', views.shopmanDetailCV, name='shopman__detail'),
    # 매장 등록 화면
    url(r'^shopman/regist/$', views.shopmanRegistCV, name='shopman__regist'),

]
