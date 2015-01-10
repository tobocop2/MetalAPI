from django.core.management.base import BaseCommand
from api.models import Band, Release, BandLineup, ReleaseLineup, BandMusician,\
        ReleaseMusician, Song, SimilarArtist, RelatedLinks
from django.core import management
from django.db import transaction
import json
import os
import glob

path = "/home/tobias/chunks/todo/*.json"
#path = "/home/tobias/chunks/*.json"
#path = "/home/tobias/chunks/ma.json"

class Command(BaseCommand):
    #args = '<foo bar ...>'
    #help = 'our help string comes here'
    #parsed_files = []

    #@transaction.atomic
    def add_bands(self):
        #bulk_bands = []
        for fname in sorted(glob.glob(path)):
            #if fname not in self.parsed_files:
            with open(fname) as data: json_data = json.load(data)
            for band in json_data:
                try:
                    ma_id = band['id']
                    print 'Trying to add id: %s' % ma_id
                    print 'In file: '+fname
                    Band.objects.get(ma_id=ma_id)
                except:
                    name = band['name']
                    print 'Adding band: %s' % name
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
                    b=Band(
                            ma_id=ma_id,
                            name=name,
                            url=url,
                            country=country,
                            status=status,
                            lyrical_themes=lyrical_themes,
                            formation_year=formation_year,
                            current_label=current_label,
                            years_active=years_active,
                            location=location, genre=genre,
                            description=description
                    )
                    #bulk_bands.append(b)
                    b.save()

                    # Create foreign key relationships for this band's albums
                    self.add_releases(band,fname)
                    self.add_band_lineups(band)
                    self.add_similar_artists(band)
                    self.add_related_links(band)

        #Band.objects.bulk_create(bulk_bands)

                #except Exception as e:
                #    if 'invalid literal' in str(e.message):
                #        with open('exceptions.log','a') as f:
                #            f.write('Error in file: %s, Band Url: %s\n Error Message: %s' % (fname, band.url, e.message))
                #    print e.message
                #    continue

            #self.parsed_files.append(fname)
            #print 'Files Parsed: %d' % len(self.parsed_files)
       # print 'Total files Parsed: %d' % len(self.parsed_files)

    def add_releases(self, band,fname):
        #bulk_releases = []
        for release in band['detailed_discography']:
            # Removing 'parsed' key to account for Tobias' horribly architected data.
            release.pop('parsed', None)

            name = release.keys()[0]
            print 'Adding release name: %s' % name
            r = Release(
                band=Band.objects.get(ma_id=band['id']),
                name=name,
                notes=release[name]['album_notes'],
                length=release[name]['length'],
                release_id=release[name]['release_id'],
                release_type=release[name]['type'],
                release_year=release[name]['year']
            )
            print 'The release '+r.band.url
            print 'The file: '+fname
            #try:
            #Release.get(release_id=r.release_id)
            r.save()
            #bulk_releases.append(r)
            self.add_songs(release, r.release_id)
            self.add_release_lineup(release, r.release_id)
            #except:
            #    continue
        #Release.objects.bulk_create(bulk_releases)

    def add_songs(self, release, release_id):
        #bulk_songs = []
        for song in release[release.keys()[0]]['songs']:
            s = Song(
                release=Release.objects.filter(release_id=release_id).first(),
                track_number=song[song.keys()[0]]['number'],
                length=song[song.keys()[0]]['length'],
                lyrics=song[song.keys()[0]]['lyrics'],
                name=song.keys()[0]
            )
            s.save()
            #bulk_songs.append(s)
        #Song.objects.bulk_create(bulk_songs)

    def add_release_lineup(self, release, release_id):
        # Create the foreign key release lineup object
        #bulk_release_musicians = []
        l = ReleaseLineup(
            release=Release.objects.filter(release_id=release_id).first(),
        )
        l.save()

        for musician in release[release.keys()[0]]['album_lineup']:
            m = ReleaseMusician(
                lineup=l,
                name=musician.keys()[0],
                role=musician[musician.keys()[0]]
            )
            m.save()
            #bulk_release_musicians.append(m)
        #ReleaseMusician.objects.bulk_create(bulk_relese_musicians)

    def add_band_lineups(self, band):
        self.add_band_lineup(band, band['lineup']['complete_lineup'], BandLineup.COMPLETE)
        self.add_band_lineup(band, band['lineup']['current_lineup'], BandLineup.CURRENT)
        self.add_band_lineup(band, band['lineup']['live_lineup'], BandLineup.LIVE)
        self.add_band_lineup(band, band['lineup']['past_lineup'], BandLineup.PAST)

    def add_band_lineup(self, band, lineup, lineup_type):
        #bulk_band_musicians = []
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
            #bulk_band_musicians.append(m)

        #BandMusician.objects.bulk_create(bulk_band_musicians)

    def add_similar_artists(self, band):
        #bulk_similar_artists = []
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
            #bulk_similar_artists.append(s)
        #SimilarArtist.objects.bulk_create(bulk_similar_artists)

    def add_related_links(self, band):
        #link_type is official,tabs etc
        #bulk_related_links = []
        fields = {
            'band': Band.objects.get(ma_id=band['id']),
        }
        for link_category in band['related_links']:
            if len(band['related_links'][link_category]) > 0:
                for link in band['related_links'][link_category]:
                    link_type = link.keys()[0]
                    url = link[link_type]
                    fields['link_type'] = link_type
                    fields['url'] = url
                    fields['category'] = link_category
                    rl = RelatedLinks(**fields)
                    rl.save()
                    #bulk_related_links.append(rl)
        #RelatedLinks.objects.bulk_create(bulk_related_links)

    def handle(self, *args, **options):
        self.add_bands()
