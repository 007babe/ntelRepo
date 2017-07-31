from django.conf.urls import url
from . import views

urlpatterns = [
    ###########################
    # Json Data
    ###########################
    # 공통코드 Json데이터 획득
    url(r'^json/comcd$', views.getJsonComCd, name='json_com_cd'),
    url(r'^json/httpstatus', views.getJsonComHttpStatus, name='json_com_http_status'),
    
    ###########################
    # Rendering
    ###########################
    # 에러페이지
    url(r'^error_popup$', views.errorPopupCV, name='error'),
]
