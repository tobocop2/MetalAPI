from django.conf.urls import patterns, url

from api import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^bands/all', views.all_bands, name='all_bands'),
    url(r'^bands/id/(?P<band_id>\d+)/$', views.bands_by_id, name='bands_by_id'),
    url(r'^bands/name/(?P<name>.+)/$', views.bands_by_name, name='bands_by_name'),
    url(r'^bands/country/(?P<country>.+)/$', views.bands_by_country, name='bands_by_country'),
    url(r'^bands/status/(?P<status>.+)/$', views.bands_by_status, name='bands_by_status'),
    url(r'^bands/lyrical_themes/(?P<lyrical_themes>.+)/$', views.bands_by_lyrical_themes, name='bands_by_lyrical_themes'),
    url(r'^bands/formation_year/(?P<year>\d+)/$', views.bands_by_year, name='bands_by_year'),
    url(r'^bands/label/(?P<label>.+)/$', views.bands_by_label, name='bands_by_label'),
    url(r'^bands/location/(?P<location>.+)/$', views.bands_by_location, name='bands_by_location'),
    url(r'^bands/genre/(?P<genre>.+)/$', views.bands_by_genre, name='bands_by_genre'),
    url(r'^bands/similarto/(?P<band_id>\d+)/$', views.bands_similar_to, name='bands_similar_to'),
    url(r'^releases/id/(?P<release_id>\d+)/$', views.releases_by_id, name='releases_by_id'),
    url(r'^releases/band_id/(?P<band_id>\d+)/$', views.releases_by_band_id, name='releases_by_band_id'),
    url(r'^releases/name/(?P<name>.+)/$', views.releases_by_name, name='releases_by_name'),
)
