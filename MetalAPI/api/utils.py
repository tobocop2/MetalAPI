def convert_band_to_dict(band):
        band_data = {}
        band_data['name'] = band.name
        band_data['ma_id'] = band.ma_id
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
