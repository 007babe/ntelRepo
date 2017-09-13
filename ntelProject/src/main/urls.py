from django.conf.urls import url

from . import views


urlpatterns = [
    ###########################
    # Rederfing
    ###########################
    # 메인화면
    url(r'^$', views.mainCV, name='index'),

    # 사용매장 변경
    url(r'^json/changeshop/$', views.jsonChangeShop, name='json__changeshop'),

    # 메뉴별 화면
    url(r'^menu/$', views.menuCV, name='menu'),  # Function Based
]
