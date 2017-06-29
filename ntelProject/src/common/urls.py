from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^comcd$', views.getComCd, name='comcd'), # 공통코드 Json데이터 획득
]
