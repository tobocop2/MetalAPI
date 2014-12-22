from django.conf.urls import patterns, url

from api import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^bands/all', views.all_bands, name='all_bands'),
    url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
)
