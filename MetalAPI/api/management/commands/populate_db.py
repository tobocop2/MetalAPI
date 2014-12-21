from django.core.management.base import BaseCommand
from api.models import Band, Release, BandLineup, ReleaseLineup, BandMusician,\
        ReleaseMusician, Song, SimilarArtists
import json
import os


data = open('/home/tobias/Q_test.json') #loading letter Q for test insertion
json_data = json.load(data)

class Command(BaseCommand):
    #args = '<foo bar ...>'
    #help = 'our help string comes here'

    def add_bands(self):
        for band in json_data:
            ma_id = band['id']
            name = band['name']
            url_name = name.replace(' ', '_')
            url = 'http://www.metal-archives.com/bands/%s/%s' % (url_name, ma_id)
            country = band['country']
            status = band['status']
            lyrical_themes = band['lyrical_themes']
            formation_year = band['formation_year']
            current_label = band['current_label']
            years_active = band['years_active']
            location = band['location']
            genre = band['genre']
            description = band['description']
            b=Band(ma_id=ma_id, name=name, url=url, country=country, status=status,\
                    lyrical_themes=lyrical_themes, formation_year=formation_year,\
                    current_label=current_label, years_active=years_active,\
                    location=location, genre=genre, description=description)
            b.save()

            # Create foreign key relationships for this band's albums
            add_releases(band)

    def add_releases(self, band):
        for release in band['detailed_discography']:
            # Removing 'parsed' key to account for Tobias' horribly architected data.
            release.pop('parsed', None)

            name = release.keys()[0]
            fields = {
                'band': Band.objects.filter(ma_id=band['ma_id']),
                'name': name,
                'notes': release[name]['album_notes'],
                'length': release[name]['length'],
                'release_id': release[name]['release_id'],
                'release_type': release[name]['type'],
                'release_year': release[name]['year']
            }

            r = Release(**fields)
            r.save()

    #def add_release(self):

    def handle(self, *args, **options):
        self.add_bands()
