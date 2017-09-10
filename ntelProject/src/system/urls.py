from django.conf.urls import url

from . import views


urlpatterns = [
    ###########################
    # Json Data
    ###########################
    # 시스템 회사 Json데이터 획득
    url(r'^json/sys_company$', views.getJsonSysCompany, name='json__sys_company'),
    # 시스템 소속 매장 Json데이터 획득
    url(r'^json/sys_shop$', views.getJsonSysShop, name='json__sys_shop'),
    # 매장 직원 Json데이터 획득
    url(r'^json/shop_staff$', views.getJsonShopStaff, name='json__shop_staff'),
    # 시스템 사용자 메뉴 Json데이터 획득
    url(r'^json/sys_menu$', views.getJsonSysMenu, name='json__sys_menu'),
    # 시스템 메세지 Json데이터 획득
    url(r'^json/sys_msg$', views.getJsonSysMsg, name='json__sys_msg'),
    ###########################
    # Rendering Page
    ###########################
]
