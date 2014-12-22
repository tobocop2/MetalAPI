from django.shortcuts import render
from django.http import HttpResponse
from api.models import Band, Release, BandLineup, ReleaseLineup, BandMusician,\
        ReleaseMusician, Song, SimilarArtist
from api.utils import convert_band_to_dict
import json

def index(request):
    return HttpResponse("Hello, world.")

def all_bands(request):
    bands = Band.objects.all()
    bands_list = []
    for band in bands:
        bands_list.append(convert_band_to_dict(band))

    return HttpResponse(json.dumps(bands_list), content_type="application/json")

def bands_by_id(request, band_id):
    bands = Band.objects.filter(ma_id=band_id)
    bands_list = []
    for band in bands:
        bands_list.append(convert_band_to_dict(band))

    return HttpResponse(json.dumps(bands_list), content_type="application/json")

def bands_by_name(request, name):
    bands = Band.objects.filter(name=name)
    bands_list = []
    for band in bands:
        bands_list.append(convert_band_to_dict(band))

    return HttpResponse(json.dumps(bands_list), content_type="application/json")

def bands_by_country(request, country):
    bands = Band.objects.filter(country=country)
    bands_list = []
    for band in bands:
        bands_list.append(convert_band_to_dict(band))

    return HttpResponse(json.dumps(bands_list), content_type="application/json")

def bands_by_status(request, status):
    bands = Band.objects.filter(status=status)
    bands_list = []
    for band in bands:
        bands_list.append(convert_band_to_dict(band))

    return HttpResponse(json.dumps(bands_list), content_type="application/json")

def bands_by_lyrical_themes(request, lyrical_themes):
    bands = Band.objects.filter(lyrical_themes=lyrical_themes)
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
    bands = Band.objects.filter(current_label=label)
    bands_list = []
    for band in bands:
        bands_list.append(convert_band_to_dict(band))

    return HttpResponse(json.dumps(bands_list), content_type="application/json")

def bands_by_location(request, location):
    bands = Band.objects.filter(location=location)
    bands_list = []
    for band in bands:
        bands_list.append(convert_band_to_dict(band))

    return HttpResponse(json.dumps(bands_list), content_type="application/json")

def bands_by_genre(request, genre):
    bands = Band.objects.filter(genre=genre)
    bands_list = []
    for band in bands:
        bands_list.append(convert_band_to_dict(band))

    return HttpResponse(json.dumps(bands_list), content_type="application/json")

def releases_by_id(request, release_id):
    releases = Release.objects.filter(release_id=release_id)
    releases_list = []
    for release in releases:
        releases_list.append(convert_release_to_dict(release))

    return HttpResponse(json.dumps(releases_list), content_type="application/json")

def releases_by_band_id(request, band_id):
    band = Band.objects.filter(ma_id=band_id)
    releases = band.release_set.all()
    releases_list = []
    for release in releases:
        releases_list.append(convert_release_to_dict(release))

    return HttpResponse(json.dumps(releases_list), content_type="application/json")
