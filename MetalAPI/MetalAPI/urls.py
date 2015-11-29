from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    # url(r'^$', include('api.urls')),
    # url(r'^api/', include('api.urls')),
    url(r'^apiv2/', include('apiv2.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
