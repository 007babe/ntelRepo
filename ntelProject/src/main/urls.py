from django.conf.urls import url

from main.views import MainView

from . import views


urlpatterns = [
    # 메인화면 
    url(r'^$', views.mainView, name='main'), # Function Based
#    url(r'^$', MainView.as_view(), name='main'), # Class Based
    
    # 컨텐츠(메뉴별)    
#    url(r'^contents/(?P<id>\w+)$', views.contentsView, name='contents'), # 메뉴별 컨텐츠 화면
    url(r'^contents/$', views.contentsView, name='contents'), # 메뉴별 컨텐츠 화면
    url(r'^contents/?\w+$', views.contentsView, name='contents'), # 메뉴별 컨텐츠 화면
]
