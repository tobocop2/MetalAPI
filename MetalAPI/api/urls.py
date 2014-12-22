from django.conf.urls import patterns, url

from api import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^bands/all', views.all_bands, name='all_bands'),
    url(r'^bands/id/(?P<ma_id>\d+)/$', views.bands_by_id, name='bands_by_id'),
    url(r'^bands/name/(?P<anystring>.+)/$', views.bands_by_name, name='bands_by_name'),
    url(r'^bands/country/(?P<anystring>.+)/$', views.bands_by_country, name='bands_by_country'),
    url(r'^bands/status/(?P<anystring>.+)/$', views.bands_by_status, name='bands_by_status'),
    url(r'^bands/lyrical_themes/(?P<anystring>.+)/$', views.bands_by_lyrical_themes, name='bands_by_lyrical_themes'),
    url(r'^bands/formation_year/(?P<anystring>.+)/$', views.bands_by_year, name='bands_by_year'),
    url(r'^bands/label/(?P<anystring>.+)/$', views.bands_by_label, name='bands_by_label'),
    url(r'^bands/location/(?P<anystring>.+)/$', views.bands_by_location, name='bands_by_location'),
    url(r'^bands/genre/(?P<anystring>.+)/$', views.bands_by_genre, name='bands_by_genre'),
)
