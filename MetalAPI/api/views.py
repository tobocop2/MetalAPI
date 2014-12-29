from django.shortcuts import render
from django.http import HttpResponse
from api.models import Band, Release, BandLineup, ReleaseLineup, BandMusician,\
        ReleaseMusician, Song, SimilarArtist,RelatedLinks
from api.utils import convert_band_to_dict, convert_release_to_dict, \
        convert_musician_set_to_dict
import json

def index(request):
    return HttpResponse("Hello, world.")

def all_band_ids(request):
    bands = Band.objects.all()
    band_ids = []
    for band in bands:
        band_ids.append({
            'id': band.ma_id,
            'band': band.name,
            'url': band.url
        })

    return HttpResponse(json.dumps(band_ids), content_type="application/json")

def bands_by_id(request, band_id):
    bands = Band.objects.filter(ma_id=band_id)
    bands_list = []
    for band in bands:
        bands_list.append(convert_band_to_dict(band))

    return HttpResponse(json.dumps(bands_list), content_type="application/json")

def bands_by_name(request, name):
    bands = Band.objects.filter(name__icontains=name)
    bands_list = []
    for band in bands:
        bands_list.append(convert_band_to_dict(band))

    return HttpResponse(json.dumps(bands_list), content_type="application/json")

def bands_by_country(request, country):
    bands = Band.objects.filter(country__iexact=country)
    bands_list = []
    for band in bands:
        bands_list.append(convert_band_to_dict(band))

    return HttpResponse(json.dumps(bands_list), content_type="application/json")

def bands_by_status(request, status):
    bands = Band.objects.filter(status__iexact=status)
    bands_list = []
    for band in bands:
        bands_list.append(convert_band_to_dict(band))

    return HttpResponse(json.dumps(bands_list), content_type="application/json")

def bands_by_lyrical_themes(request, lyrical_themes):
    bands = Band.objects.filter(lyrical_themes__icontains=lyrical_themes)
    bands_list = []
    for band in bands:
        bands_list.append(convert_band_to_dict(band))

    return HttpResponse(json.dumps(bands_list), content_type="application/json")

def bands_by_year(request, year):
    bands = Band.objects.filter(formation_year=year)
    bands_list = []
    for band in bands:
        bands_list.append(convert_band_to_dict(band))

    return HttpResponse(json.dumps(bands_list), content_type="application/json")

def bands_by_label(request, label):
    bands = Band.objects.filter(current_label__icontains=label)
    bands_list = []
    for band in bands:
        bands_list.append(convert_band_to_dict(band))

    return HttpResponse(json.dumps(bands_list), content_type="application/json")

def bands_by_location(request, location):
    bands = Band.objects.filter(location__icontains=location)
    bands_list = []
    for band in bands:
        bands_list.append(convert_band_to_dict(band))

    return HttpResponse(json.dumps(bands_list), content_type="application/json")

def bands_by_genre(request, genre):
    bands = Band.objects.filter(genre__icontains=genre)
    bands_list = []
    for band in bands:
        bands_list.append(convert_band_to_dict(band))

    return HttpResponse(json.dumps(bands_list), content_type="application/json")

def bands_by_musician(request, musician):
    bands_list = []
    for band in Band.objects.all():
        for lineup in band.bandlineup_set.all():
            for musician in lineup.bandmusician_set.filter(name__icontains=musician):
                musicians_band = musician.lineup.band
                bands_list.append(convert_band_to_dict(musicians_band))

    return HttpResponse(json.dumps(bands_list), content_type="application/json")

def bands_similar_to(request, band_id):
    original_band = Band.objects.get(ma_id=band_id)
    bands_list = []
    for similar_band in original_band.similarartist_set.all():
        band = Band.objects.filter(ma_id=similar_band.ma_id).first()
        if band:
            band_dict = convert_band_to_dict(band)
            bands_list.append(band_dict)

    return HttpResponse(json.dumps(bands_list), content_type="application/json")

def releases_by_id(request, release_id):
    releases = Release.objects.filter(release_id=release_id)
    releases_list = []
    for release in releases:
        releases_list.append(convert_release_to_dict(release))

    return HttpResponse(json.dumps(releases_list), content_type="application/json")

def releases_by_band_id(request, band_id):
    band = Band.objects.get(ma_id=band_id)
    releases = band.release_set.all()
    releases_list = []
    for release in releases:
        releases_list.append(convert_release_to_dict(release))

    return HttpResponse(json.dumps(releases_list), content_type="application/json")

def releases_by_name(request, name):
    releases = Release.objects.filter(name__icontains=name)
    releases_list = []
    for release in releases:
        releases_list.append(convert_release_to_dict(release))

    return HttpResponse(json.dumps(releases_list), content_type="application/json")

def lineups_by_band(request, band_id):
    band = Band.objects.get(ma_id=band_id)
    lineups_data = {}
    lineups_data['band'] = band.name
    lineups_data['band_id'] = band.ma_id

    # Dict pairing model enums with their user friendly representations.
    lineup_types = {}
    for lineup_type in BandLineup.LINEUP_TYPES:
        lineup_types[lineup_type[0]] = lineup_type[1]
        lineups_data[lineup_type[1]] = []

    # Iterate through each lineup for the band.
    for lineup in band.bandlineup_set.all():
        lineup_type = lineup_types[lineup.lineup_type]
        lineups_data[lineup_type].append(convert_musician_set_to_dict(lineup))

    return HttpResponse(json.dumps(lineups_data), content_type="application/json")
