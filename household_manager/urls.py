from django.conf.urls import url
from . import views

app_name = 'household_manager'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^manage/(?P<filename>\w+.json)/$', views.manage, name='manage'),
    url(r'^choose/$', views.choose, name='choose'),
]
