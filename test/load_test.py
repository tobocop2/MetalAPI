import requests
import json
import os

base_url = 'http://perelste.in:8001/api'

def make_dir(dir_name,unique_id):
    dir_name = '%s - %s' % (dir_name.replace('/','\\').encode('ascii','ignore'), unique_id)
    try:
        #os.makedirs(dir_name)
        os.makedirs(dir_name)
    except OSError:
        if not os.path.isdir(dir_name):
            raise
    return dir_name


def get_band_data(base_url):
    all_bands = requests.get('%s/bands/all' % base_url)

    os.chdir(make_dir('Bands',len(all_bands.json())))
    for band in all_bands.json():
        print 'Getting file for %s' % band['band']
        os.chdir(make_dir(band['band'],band['id']))
        get_bands_by_id(base_url,band['band'],band['id'])
        get_releases_by_id(base_url,band['id'])
        get_lineups_by_id(base_url,band['id'])
        os.chdir('../')

def get_bands_by_id(base_url,band_name,band_id):
    band_by_id = requests.get('%s/bands/id/%s' % (base_url,str(band_id))).json()
    band_name = band_name.replace('/','\\').encode('ascii','ignore')
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
