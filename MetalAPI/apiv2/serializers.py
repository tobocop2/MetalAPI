from .models import (
    Band,
    Lineup,
    Release,
    Musician,
    Track,
    RelatedLink
)
from rest_framework import serializers


class BandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Band
        fields = (
            'ma_id',
            'name',
            'url',
            'country',
            'status',
            'lyrical_themes',
            'formation_year',
            'current_label',
            'years_active',
            'location',
            'genre',
            'description',
            'similar_bands',
            # 'related_links',
            # 'releases',
            # 'lineup'
        )


class LineupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lineup
        fields = ('lineup_type', 'musicians')


class TrackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Track
        fields = ('name', 'track_number', 'length', 'lyrics')


class ReleaseSerializer(serializers.HyperlinkedModelSerializer):
    tracks = TrackSerializer(many=True)

    class Meta:
        model = Release
        fields = (
            'lineup',
            'name',
            'notes',
            'length',
            'ma_release_id',
            'release_type',
            'release_year',
            'release_category',
            'tracks'
        )


class MusicianSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Musician
        fields = ('name', 'role')


class RelatedLinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RelatedLink
        fields = ('category', 'link_type', 'url')
