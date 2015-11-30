from .models import (
    Band,
    Lineup,
    Release,
    Musician,
    Track,
    RelatedLink
)
from rest_framework import serializers


class MusicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musician
        fields = ('id', 'name', 'role', 'url')


class LineupSerializer(serializers.ModelSerializer):
    musicians = MusicianSerializer(many=True)

    class Meta:
        model = Lineup
        fields = ('id', 'lineup_type', 'musicians', 'url', 'releases')

    def create(self, validated_data):
        musicians_data = validated_data.pop('musicians')
        releases_data = validated_data.pop('releases')
        lineup = Lineup.objects.create(**validated_data)
        for musician_data, release_data in zip(musicians_data, releases_data):
            musician = Musician.objects.\
                filter(ma_musician_id=musician_data['ma_musician_id']).\
                first()
            release = Release.objects.\
                filter(ma_release_id=release_data['ma_release_id']).\
                first()
            if not musician and not release:
                Musician.objects.create(lineup=lineup, **musician_data)
                Release.objects.create(lineup=lineup, **release_data)
            elif not musician:
                Musician.objects.create(lineup=lineup, **musician_data)
                lineup.release_set.add(musician)
            elif not release:
                Release.objects.create(lineup=lineup, **release_data)
                lineup.musician_set.add(musician)
            else:
                lineup.release_set.add(musician)
                lineup.musician_set.add(musician)

        return lineup


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ('id', 'name', 'track_number', 'length', 'lyrics', 'url')


class ReleaseSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True)

    class Meta:
        model = Release
        fields = (
            'id',
            'name',
            'notes',
            'length',
            'ma_release_id',
            'release_type',
            'release_year',
            'release_category',
            'tracks',
            'url'
        )

    def create(self, validated_data):
        tracks_data = validated_data.pop('tracks')
        release = Release.objects.create(**validated_data)
        for track_data in tracks_data:
            Track.objects.create(release=release, **track_data)
        return release


class RelatedLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedLink
        fields = ('id', 'category', 'link_type', 'url')


class BandSerializer(serializers.ModelSerializer):
    related_links = RelatedLinkSerializer(many=True)
    lineups = LineupSerializer(many=True)
    similar_bands = serializers.SlugRelatedField(many=True,
                                                 read_only=True,
                                                 slug_field='name')

    class Meta:
        model = Band
        fields = (
            'id',
            'ma_id',
            'name',
            'ma_url',
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
            'related_links',
            'lineups'
        )

    def create(self, validated_data):
        related_link_data = validated_data.pop('related_links')
        lineup_data = validated_data.pop('lineups')
        band = Band.objects.create(**validated_data)
        for lineup_data, related_link_data in zip(lineup_data,
                                                  related_link_data):
            Lineup.objects.create(band=band, **lineup_data)
            RelatedLink.objects.create(band=band, **related_link_data)
        return band
