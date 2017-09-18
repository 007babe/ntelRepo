from django.conf.urls import url

from . import views


urlpatterns = [
    ###########################
    # Login/Logout
    ###########################
    url(r'^login$', views.loginCV, name='login'),  # 로그인 화면
    url(r'^loginpop$', views.loginPopCV, name='loginpop'),  # 로그인POP 화면
    url(r'^logincheck$', views.loginCheckCV, name='logincheck'),  # 로그인 체크
    url(r'^logout$', views.logoutCV, name='logout'),  # 로그아웃 화면

    # 아이디/비번 찾기
    url(r'^findId$', views.logoutCV, name='findId'),  # ID 찾기
    url(r'^findPw$', views.logoutCV, name='findPw'),  # Password 찾기




]
