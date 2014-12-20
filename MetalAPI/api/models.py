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
    releases = None # Come back to this.
    similar_artists = None # Come back to this.
    line_up = None # Come back to this.
