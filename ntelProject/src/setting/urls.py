from django.conf.urls import url

from . import views


urlpatterns = [
    #===============================>
    # 거래처관리
    #===============================<

    #===============================>
    # 직원관리
    #===============================<
    # 직원 리스트(Json)
    url(r'^staffman/json/list/$', views.staffmanJsonList, name='staffman__json__list'),
    # 직원 정보 수정(Json)
    url(r'^staffman/json/modify/$', views.staffmanJsonModify, name='staffman__json__modify'),
    # 직원 상세 화면
    url(r'^staffman/detail/$', views.staffmanDetailCV, name='staffman__detail'),
    # 직원 등록 화면
    url(r'^staffman/regist/$', views.staffmanRegistCV, name='staffman__regist'),
]
