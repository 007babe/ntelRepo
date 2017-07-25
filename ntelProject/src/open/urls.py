from django.conf.urls import url

from . import views

urlpatterns = [
    # 전체개통
#    url(r'^total/$', views.openTotalCV, name='total'), # 전체개통

    # 신규개통
    url(r'^new/tab1/$', views.openNewTab1CV, name='new_tab1'), # 신규개통 : 단말기
    url(r'^new/tab2/$', views.openNewTab2CV, name='new_tab2'), # 신규개통 : 유심/중고
    url(r'^new/tab3/$', views.openNewTab3CV, name='new_tab3'), # 신규개통 : 홈/인터넷
    
#    url(r'^history/$', views.openHistoryCV, name='new'), # 개통처리이력
]
