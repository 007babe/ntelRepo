from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^json/comcd$', views.getJsonComCd, name='json_com_cd'), # 공통코드 Json데이터 획득
]
