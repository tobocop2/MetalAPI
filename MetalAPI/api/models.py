from django.db import models

# Create your models here.

class Band(models.Model):
    ma_id = models.IntegerField()
    name = models.CharField(max_length=200)
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
    releases = None # List of foreign keys to Release
    similar_artists = None # Come back to this.
    complete_line_up = None # List of foreign keys to Lineup
    current_lineup = None # Foreign key to Lineup
    live_lineup = None # Foreign key to Lineup
    past_lineup = None # Foreign key to Lineup

class Release(models.Model):
    name = models.CharField(max_length=200)
    notes = models.TextField()
    length = models.CharField(max_length=200)
    release_id = models.IntegerField()
    release_type = models.CharField(max_length=200)
    release_year = models.IntegerField()
    songs = None # List of foreign keys to Song.
    line_up = None # Foreign key to Lineup.

class Lineup(models.Model):
    musicians = None # List of foreign keys to Musician

class Musician(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
