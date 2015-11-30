from django.conf.urls import url, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'bands', views.BandViewSet)
router.register(r'lineups', views.LineupViewSet)
router.register(r'releases', views.ReleaseViewSet)
router.register(r'musicians', views.MusicianViewSet)
router.register(r'tracks', views.TrackViewSet)
router.register(r'relatedlinks', views.RelatedLinkViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework'))
]
