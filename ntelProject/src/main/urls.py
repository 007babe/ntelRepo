from django.conf.urls import url

from . import views


urlpatterns = [
    ###########################
    # Rederfing
    ###########################
    # 메인화면
    url(r'^$', views.mainCV, name='index'),

    # 사용매장 변경
    url(r'^json/changeshop/$', views.jsonChangeShop, name='json__changeshop'),

    # 메뉴별 화면
    url(r'^menu/$', views.menuCV, name='menu'),  # Function Based

    # 사용자정보 화면
    url(r'^user_info/detail$', views.userInfoDetailCV, name='user_info__detail'),  # 사용자정보 상세 화면
    url(r'^user_info/json/modify$', views.userInfoJsonModify, name='user_info__json__modify'),  # 사용자정보 변경 처리

    # 비밀번호 변경 화면
    url(r'^change_password/detail$', views.changePasswordDetailCV, name='change_password__detail'),  # 비밀번호 변경 화면
    url(r'^change_password/json/modify$', views.changePasswordJsonModify, name='change_password__json__modify'),  # 비밀번호 변경 처리
]
