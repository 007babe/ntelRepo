from django.conf.urls import url
from . import views

urlpatterns = [
    ###########################
    # Json Data
    ###########################

    ###########################
    # Rendering
    ###########################
    # 에러페이지
    url(r'^error_popup$', views.errorPopupCV, name='error'),
]
