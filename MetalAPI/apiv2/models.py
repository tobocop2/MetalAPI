from django.db import models


class Band(models.Model):
    similar_artists = models.ManyToManyField('self', through='SimilarBand',
                                             symmetrical=False,
                                             related_name='similar_to')
    ma_id = models.BigIntegerField()
    name = models.TextField()
    url = models.URLField()
    country = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    lyrical_themes = models.CharField(max_length=200)
    formation_year = models.CharField(max_length=200)
    current_label = models.CharField(max_length=200)
    years_active = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    description = models.TextField()


class SimilarBand(models.Model):
    from_band = models.ForeignKey(Band, related_name='from_bands')
    to_band = models.ForeignKey(Band, related_name='to_bands')


class Lineup(models.Model):
    CURRENT = 'CR'
    LIVE = 'LI'
    PAST = 'PA'
    UNKNOWN = 'UN'
    LINEUP_TYPES = (
        (CURRENT, 'current'),
        (LIVE, 'live'),
        (PAST, 'past'),
        (UNKNOWN, 'unknown'),
    )

    band = models.ForeignKey(Band)
    lineup_type = models.CharField(max_length=2, choices=LINEUP_TYPES)


class Release(models.Model):
    lineup = models.ForeignKey(Lineup)
    name = models.TextField()
    notes = models.TextField()
    length = models.CharField(max_length=200)
    release_id = models.BigIntegerField()
    release_type = models.CharField(max_length=200)
    release_year = models.IntegerField()
    release_category = models.CharField(max_length=200)


class Musician(models.Model):
    name = models.TextField()
    role = models.TextField()
    lineup = models.ManyToManyField(Lineup)


class Song(models.Model):
    release = models.ForeignKey(Release)
    track_number = models.IntegerField()
    name = models.TextField()
    length = models.CharField(max_length=200)
    lyrics = models.TextField()


class RelatedLink(models.Model):
    band = models.ForeignKey(Band)
    category = models.CharField(max_length=200)
    link_type = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
