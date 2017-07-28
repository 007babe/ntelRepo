from django.conf.urls import url

from . import views


urlpatterns = [
    # Json Data
    url(r'^json/syscompany$', views.getJsonSysCompany, name='json_sys_company'), # 시스템 회사 Json데이터 획득
    url(r'^json/shopstaff$', views.getJsonShopStaff, name='json_shop_staff'), # 매장 직원 Json데이터 획득
    url(r'^json/sysmenu$', views.getJsonSysMenu, name='json_sys_menu'), # 시스템 사용자 메뉴 Json데이터 획득
    url(r'^json/sysmsg$', views.getJsonSysMsg, name='json_sys_msg'), # 시스템 메세지 Json데이터 획득
    
]
