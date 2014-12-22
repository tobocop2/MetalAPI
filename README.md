MetalAPI
========

A REST API for the Metal Archives(http://www.metal-archives.com/), the largest encyclopedic resource for heavy metal music.

This API allows you to have access to all of the data from the "Encyclopaedia Metallum" including every metal band, their releases, lineups and all metadata. We personally scraped the entire archives, so now all metalhead hackers or data enthusiasts can develop awesome things

## Table of Contents

 - [Endpoints](#endpoints)
    - [Bands](#bands)
        - [All](#all)
        - [ID](#id)
        - [Name](#name)
        - [Country](#country)
        - [Status](#status)
        - [Lyrical Themes](#lyrical themes)
        - [Formation Year](#formation year)
        - [Label](#label)
        - [Location](#Location)
        - [Genre](#Genre)
        - [Similar to](#similar to)
    - [Releases(albums)](#releases)
        - [Band ID](#band id)
        - [Release ID](#release id)
        - [Name](#name)

## Endpoints

### Bands

#### All
URL: `/api/bands/all`
Retrieves all bands from the Metal Archives currently in our database.
#### ID
URL: `/api/bands/id/<band_id>`
Retrieves the band whose Metal Archives ID corresponds to `band_id`.
#### Name
URL: `/api/bands/name/<band_name>`
Retrieves all bands whose name contains the string given in the route as `band_name`.
#### Country
URL: `/api/bands/country/<country>`
Retrieves all bands from `country`.
#### Status
URL: `/api/bands/status/<status>`
Retrieves all bands whose current activity status is `status`.
#### Lyrical Themes
URL: `/api/bands/lyrical_themes/<theme>`
Retrieves all bands whose lyrical themes contain the string given in the route as `theme`.
#### Formation Year
URL: `/api/bands/formation_year/<year>`
Retrieves all bands who were formed in `year`.
#### Label
URL: `/api/bands/label/<current_label>`
Retrieves all bands who are currently signed to `current_label`.
#### Location
URL: `/api/bands/location/<location>`
Retrieves all bands from `location`.
#### Genre
URL: `/api/bands/genre/<genre>`
Retrieves all bands have a genre of `genre`.
#### Similar To
URL: `/api/bands/similarto/<band_name>`
Retrieves all bands whose similar artists contain the band, `band_name`.
This is extremely useful for finding relationships between bands.


### Releases

#### Release ID
URL: `/api/releases/id/<release ide>`
Retrieves all albums/releases corresponding to the Metal Archives ID of `release_id`.
#### Band ID
URL: `/api/releases/band_id/<band ide>`
Retrieves all albums/releases released by the band corresponding to `band_id`.
#### name
URL: `/api/releases/name/<release name>`
Retrieves all albums/releases whose name contains the string given in the route as `release_name`.
