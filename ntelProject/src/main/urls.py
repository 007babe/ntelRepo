from django.conf.urls import url

from main.views import MainView

from . import views


urlpatterns = [
    # 메인화면 
    url(r'^$', views.mainView, name='main'), # Function Based
#    url(r'^$', MainView.as_view(), name='main'), # Class Based
]
