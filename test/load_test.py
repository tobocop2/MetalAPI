import requests
import json
import os

base_url = 'http://perelste.in:8001/api'

def make_dir(dir_name):
    try:
        os.makedirs(dir_name.replace('/','\\')
    except OSError:
        if not os.path.isdir(dir_name):
            raise

def get_band_data(base_url):
    all_bands = requests.get('%s/bands/all' % base_url)

    make_dir('Bands')
    os.chdir('Bands')
    for band in all_bands.json():
        print 'Getting file for %s' % band['band']
        make_dir(band['band'])
        os.chdir(band['band'])
        get_bands_by_id(base_url,band['band'],band['id'])
        get_releases_by_id(base_url,band['id'])
        get_lineups_by_id(base_url,band['id'])
        os.chdir('../')

def get_bands_by_id(base_url,band_name,band_id):
    band_by_id = requests.get('%s/bands/id/%s' % (base_url,str(band_id))).json()
    with open('%s_info.json' % band_name,'w') as json_file:
        json.dump(band_by_id,json_file)

def get_releases_by_id(base_url,band_id):
    releases_by_id = requests.get('%s/releases/id/%s' % (base_url,str(band_id))).json()
    with open('release_info.json','w') as json_file:
        json.dump(releases_by_id,json_file)

def get_lineups_by_id(base_url,band_id):
    lineups_by_id = requests.get('%s/lineups/%s' % (base_url,str(band_id))).json()
    with open('lineup_info.json','w') as json_file:
        json.dump(lineups_by_id,json_file)

if __name__ == "__main__":
    get_band_data(base_url)
