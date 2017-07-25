from django.conf.urls import url

from home.views import IndexView, HomeView


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^home$', HomeView.as_view(), name='home'),
]
