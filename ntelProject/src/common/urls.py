from django.conf.urls import url
from . import views

urlpatterns = [
    ###########################
    # Json Data
    ###########################
    # 공통코드 Json데이터 획득
    url(r'^json/com_cd$', views.getJsonComCd, name='json__comcd'),
    url(r'^json/com_http_status', views.getJsonComHttpStatus, name='json__com_http_status'),

    ###########################
    # Rendering
    ###########################
    # 에러페이지
    url(r'^error_popup$', views.errorPopupCV, name='error'),
]
