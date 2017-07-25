from django.conf.urls import url

from . import views

urlpatterns = [
    # 메인화면 
    url(r'^$', views.mainCV, name='main'), # Function Based
#    url(r'^$', MainView.as_view(), name='main'), # Class Based

    # 메뉴별 화면 
    url(r'^menu/$', views.menuCV, name='menu'), # Function Based
]
