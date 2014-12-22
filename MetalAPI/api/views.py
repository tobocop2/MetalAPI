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

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)
