def convert_band_to_dict(band):
    band_data = {}
    band_data['name'] = band.name
    band_data['id'] = band.ma_id
    band_data['url'] = band.url
    band_data['country'] = band.country
    band_data['genre'] = band.genre
    band_data['status'] = band.status
    band_data['lyrical_themes'] = band.lyrical_themes
    band_data['formation_year'] = band.formation_year
    band_data['years_active'] = band.years_active
    band_data['location'] = band.location
    band_data['description'] = band.description
    return band_data

def convert_release_to_dict(release):
    release_data = {}
    release_data['band'] = release.band.name
    release_data['band_id'] = release.band.ma_id
    release_data['band_url'] = release.band.url
    release_data['name'] = release.name
    release_data['notes'] = release.notes
    release_data['length'] = release.length
    release_data['release_id'] = release.release_id
    release_data['release_type'] = release.release_type
    release_data['release_year'] = release.release_year
    return band_data

def convert_band_lineup_to_dict(release):
    band_lineup_data = {}
    return band_lineup_data
