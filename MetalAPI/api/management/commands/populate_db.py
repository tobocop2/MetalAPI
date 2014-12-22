from django.core.management.base import BaseCommand
from api.models import Band, Release, BandLineup, ReleaseLineup, BandMusician,\
        ReleaseMusician, Song, SimilarArtist
from django.core import management
import json
import os

management.call_command('flush')
data = open('/home/tobias/json/Q_test.json') #loading letter Q for test insertion
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
            self.add_releases(band)
            self.add_band_lineups(band)
            self.add_similar_artists(band)

    def add_releases(self, band):
        for release in band['detailed_discography']:
            # Removing 'parsed' key to account for Tobias' horribly architected data.
            release.pop('parsed', None)

            name = release.keys()[0]
            r = Release(
                band=Band.objects.get(ma_id=band['id']),
                name=name,
                notes=release[name]['album_notes'],
                length=release[name]['length'],
                release_id=release[name]['release_id'],
                release_type=release[name]['type'],
                release_year=release[name]['year']
            )

            r.save()
            self.add_songs(release, r.release_id)
            self.add_release_lineup(release, r.release_id)

    def add_songs(self, release, release_id):
        for song in release[release.keys()[0]]['songs']:
            s = Song(
                release=Release.objects.get(release_id=release_id),
                track_number=song[song.keys()[0]]['number'],
                length=song[song.keys()[0]]['length'],
                lyrics=song[song.keys()[0]]['lyrics'],
                name=song.keys()[0]
            )

            s.save()

    def add_release_lineup(self, release, release_id):
        # Create the foreign key release lineup object
        l = ReleaseLineup(
            release=Release.objects.get(release_id=release_id),
        )
        l.save()

        for musician in release[release.keys()[0]]['album_lineup']:
            m = ReleaseMusician(
                lineup=l,
                name=musician.keys()[0],
                role=musician[musician.keys()[0]]
            )

            m.save()

    def add_band_lineups(self, band):
        self.add_band_lineup(band, band['lineup']['complete_lineup'], BandLineup.COMPLETE)
        self.add_band_lineup(band, band['lineup']['current_lineup'], BandLineup.CURRENT)
        self.add_band_lineup(band, band['lineup']['live_lineup'], BandLineup.LIVE)
        self.add_band_lineup(band, band['lineup']['past_lineup'], BandLineup.PAST)

    def add_band_lineup(self, band, lineup, lineup_type):
        l = BandLineup(
            band=Band.objects.get(ma_id = band['id']),
            lineup_type=lineup_type
        )

        l.save()

        for musician in lineup:
            m = BandMusician(
                lineup=l,
                name=musician.keys()[0],
                role=musician[musician.keys()[0]]
            )

            m.save()

    def add_similar_artists(self, band):
        for artist in band['similar_artists']:
            fields = {
                'name': artist.keys()[0],
                'band': Band.objects.get(ma_id=band['id'])
            }
            for info in artist[fields['name']]:
                if info.keys()[0] == 'country':
                    fields['country'] = info['country']
                if info.keys()[0] == 'genre':
                    fields['genre'] = info['genre']
                if info.keys()[0] == 'url':
                    fields['url'] = info['url']
                    ma_id = info['url'].split('/')[-1]
                    fields['ma_id'] = ma_id
                    #fields['similar_band'] = Band.objects.get(ma_id=ma_id)

            s = SimilarArtist(**fields)
            s.save()

    def handle(self, *args, **options):
        self.add_bands()
