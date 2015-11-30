from .models import (
    Band,
    Lineup,
    Release,
    Musician,
    Track,
    RelatedLink
)
from .serializers import (
    BandSerializer,
    LineupSerializer,
    ReleaseSerializer,
    MusicianSerializer,
    TrackSerializer,
    RelatedLinkSerializer
)
from rest_framework import viewsets


class BandViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bands to be viewed or edited.
    """
    queryset = Band.objects.all().order_by('-ma_id')
    serializer_class = BandSerializer


class LineupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows lineups to be viewed or edited.
    """
    queryset = Lineup.objects.all()
    serializer_class = LineupSerializer


class ReleaseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows releases to be viewed or edited.
    """
    queryset = Release.objects.all().order_by('-release_year')
    serializer_class = ReleaseSerializer


class MusicianViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows musicians to be viewed or edited.
    """
    queryset = Musician.objects.all().order_by('name')
    serializer_class = MusicianSerializer


class TrackViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows songs to be viewed or edited.
    """
    queryset = Track.objects.all().order_by('name')
    serializer_class = TrackSerializer


class RelatedLinkViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows related links to be viewed or edited.
    """
    queryset = RelatedLink.objects.all().order_by('category')
    serializer_class = RelatedLinkSerializer
