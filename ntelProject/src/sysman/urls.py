from django.conf.urls import url
from . import views

urlpatterns = [
    # 사용관리
    url(r'^use/tab1/$', views.sysmanUseTab1CV, name='use_tab1'), # 이용신청관리
    url(r'^use/tab2/$', views.sysmanUseTab1CV, name='use_tab2'), # 사용회사관리
    url(r'^use/tab3/$', views.sysmanUseTab2CV, name='use_tab3'), # 사용자관리
    
    # 메뉴관리
#    url(r'^menu/tab1/$', views.sysmanMenuTab1CV, name='menu_tab1'), # 메뉴관리
]
