from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.appReqCV, name='index'),  # 이용신청화면
    url(r'^regist$', views.appReqRegistSV, name='regist'),  # 이용신청요청
    url(r'^result$', views.appReqResultPopCV, name='result'),  # 이용신청결과

    # 아이디 중복 체크
    url(r'^json/is_usable_id$', views.getJsonIsUsableId, name='json__is_usable_id'),
]
