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
    # 직원 상세 화면
    url(r'^staffman/detail/$', views.staffmanDetailCV, name='staffman__detail'),
    # 직원 등록 화면
    url(r'^staffman/regist/$', views.staffmanRegistCV, name='staffman__regist'),


    # 이용신청관리 승인/취소 처리(Json)
#    url(r'^useman/appreqman/json/appr$', views.appreqmanJsonAppr, name='useman__appreqman__json_appr'),
    # 이용신청관리 상세 화면
#    url(r'^useman/appreqman/detail/$', views.appreqmanDetailCV, name='useman__appreqman__detail'),
    
    
    
    # 미결업무목록
#    url(r'^list/$', views.listCV, name='list'), # 미결업무목록
]
