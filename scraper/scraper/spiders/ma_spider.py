from scrapy.spider import Spider
from scrapy.http import Request
from xtr33m.items import band_item
from bs4 import BeautifulSoup,UnicodeDammit
import string
import time
import json
import re

START_URL_FMT = 'http://www.metal-archives.com/browse/ajax-letter/l/{}/json/1?sEcho=1&iColumns=4&sColumns=&iDisplayStart=0&iDisplayLength=500&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&iSortCol_0=0&sSortDir_0=asc&iSortingCols=1&bSortable_0=true&bSortable_1=true&bSortable_2=true&bSortable_3=false&_={}'
NEXT_URL_FMT = 'http://www.metal-archives.com/browse/ajax-letter/l/{}/json/1?sEcho=1&iColumns=4&sColumns=&iDisplayStart={}&iDisplayLength=500&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&iSortCol_0=0&sSortDir_0=asc&iSortingCols=1&bSortable_0=true&bSortable_1=true&bSortable_2=true&bSortable_3=false&_={}'
total_bands = []

class ma_spider(Spider):
    name = "ma"
    allowed_domains = ["www.metal-archives.com"]

    def start_requests(self):
        #letters = ['NBR']+list(string.uppercase)
        letters = ['Z']
        for letter in letters:
            #passing in the letter and the time into the url
            url = START_URL_FMT.format(letter,int(time.time()))
            #using this for the next url format
            meta = {'letter': letter}
            yield Request(url,callback=self.parse_first,meta=meta)


    def parse_first(self, response):
        jsonresponse = json.loads(response.body)
        total = jsonresponse['iTotalRecords']
        for i in range(0,total,500):
            url = NEXT_URL_FMT.format(response.meta['letter'], i, int(time.time()))
            yield Request(url, callback=self.parse_json)


    def parse_json(self,response):
        jsonresponse = json.loads(response.body)
        for item in range(0,len(jsonresponse["aaData"])):
            soup = BeautifulSoup(jsonresponse["aaData"][item][0])
            band_link = soup.select('a')[0]['href']
            band_name = soup.text.encode('utf-8')
            #total_bands.append(band_name.encode('ascii','ignore'))
            yield Request(band_link,callback=self.parse_band)

    def parse_band(self,response):
        soup = BeautifulSoup(response.body)
        item = band_item()

        band_name = soup.select('.band_name')[0].text.encode('utf-8')
        band_id = response.url.split('/')[-1]
        country = soup.select('#band_stats dd')[0].text.encode('utf-8')
        location = soup.select('#band_stats dd')[1].text.encode('utf-8')
        status = soup.select('#band_stats dd')[2].text.encode('utf-8')
        formation = soup.select('#band_stats dd')[3].text.encode('utf-8')
        genre = soup.select('#band_stats dd')[4].text.encode('utf-8')
        lyrical_themes = soup.select('#band_stats dd')[5].text.encode('utf-8')
        current_label = soup.select('#band_stats dd')[6].text.encode('utf-8')
        years_active = soup.select('#band_stats dd')[7].text.encode('utf-8')
        years_active = ''.join([c for c in years_active if c not in '\n\t '])
        desc_comment = 'Max 400 characters. Open the rest in a dialogue box'

        item['name'] = band_name
        item['id'] = band_id
        item['country'] =country
        item['location'] = location
        item['status'] = status
        item['formation_year'] = formation
        item['genre'] = genre
        item['lyrical_themes'] =lyrical_themes
        item['current_label'] = current_label
        item['years_active'] = years_active
        item['description'] = ''

        #if '\nRead more\n' not in soup.findAll(attrs={'class': re.compile(r".*\bband_comment\b.*")})[0].text.encode('utf-8'):
        raw_description = soup.findAll(attrs={'class': re.compile(r".*\bband_comment\b.*")})[0].text.encode('utf-8').strip()
        description = ''.join(c for c in raw_description if not c in '\n\r\t')
        if desc_comment in description:
            item['description'] = description.replace(desc_comment,'')
        else:
            item['description'] = description

        item['lineup'] = {'complete_lineup': [],'current_lineup': [],'past_lineup': [],'live_lineup': []}
        if soup.find_all(id=['band_tab_members_all','band_tab_members_current','band_tab_members_past','band_tab_members_live']) is not None:
            lineup = soup.select('#band_tab_members_all .lineupRow td a')
            if len(lineup)> 0:
                role_soup = soup.select('#band_tab_members_all .lineupRow td')
                roles = role_soup[1:len(role_soup):2]
                roles = [''.join(re.split('\t|\n',role.text)) for role in roles]
                for member,role, in zip(lineup,roles):
                    #band_member = member.text.encode('utf-8')+' - '+role.encode('utf-8')
                    if not item['lineup']['complete_lineup']:
                        item['lineup']['complete_lineup'] = [{member.text.encode('utf-8'): role.encode('utf-8')}]
                    else:
                        item['lineup']['complete_lineup'].append({member.text.encode('utf-8'): role.encode('utf-8')})
            #current linup
            lineup = soup.select('#band_tab_members_current .lineupRow td a')
            if len(lineup)> 0:
                role_soup = soup.select('#band_tab_members_current .lineupRow td')
                roles = role_soup[1:len(role_soup):2]
                roles = [''.join(re.split('\t|\n',role.text)) for role in roles]
                for member,role, in zip(lineup,roles):
                    #band_member = member.text.encode('utf-8')+' - '+role.encode('utf-8')
                    if not item['lineup']['current_lineup']:
                        item['lineup']['current_lineup'] = [{member.text.encode('utf-8'): role.encode('utf-8')}]
                    else:
                        item['lineup']['current_lineup'].append({member.text.encode('utf-8'): role.encode('utf-8')})
            #past lineup
            lineup = soup.select('#band_tab_members_past .lineupRow td a')
            if len(lineup)> 0:
                role_soup = soup.select('#band_tab_members_past .lineupRow td')
                roles = role_soup[1:len(role_soup):2]
                roles = [''.join(re.split('\t|\n',role.text)) for role in roles]
                for member,role, in zip(lineup,roles):
                    #band_member = member.text.encode('utf-8')+' - '+role.encode('utf-8')
                    if not item['lineup']['past_lineup']:
                        item['lineup']['past_lineup'] = [{member.text.encode('utf-8'): role.encode('utf-8')}]
                    else:
                        item['lineup']['past_lineup'].append({member.text.encode('utf-8'): role.encode('utf-8')})
            #live lineup
            lineup = soup.select('#band_tab_members_live .lineupRow td a')
            if len(lineup)> 0:
                role_soup = soup.select('#band_tab_members_live .lineupRow td')
                roles = role_soup[1:len(role_soup):2]
                roles = [''.join(re.split('\t|\n',role.text)) for role in roles]
                for member,role, in zip(lineup,roles):
                    band_member = member.text.encode('utf-8')+' - '+role.encode('utf-8')
                    if not item['lineup']['live_lineup']:
                        item['lineup']['live_lineup'] = [{member.text.encode('utf-8'): role.encode('utf-8')}]
                    else:
                        item['lineup']['live_lineup'].append({member.text.encode('utf-8'): role.encode('utf-8')})
        band_desc_url = 'http://www.metal-archives.com/band/read-more/id/%s' % band_id
        yield Request(band_desc_url,callback=self.parse_description,meta={'item':item})

    def parse_description(self,response):
        #something wrong here
        item = response.meta['item']
        soup = BeautifulSoup(response.body)
        print 'description before:\t'+item['description']
        #for description in soup.find_all(text=True):
        long_desc = ''.join(c for c in soup.text.strip() if not c in '\r\t').replace('\n',' ')
        if 'Read more' in item['description']:
            item['description'] = long_desc
        print 'description after:\t'+item['description']
        sa_url = 'http://www.metal-archives.com/band/ajax-recommendations/id/%s/showMoreSimilar/1' % item['id']
        yield Request(sa_url,callback=self.parse_similar_artists,meta={'item':item})

    def parse_similar_artists(self,response):
        #similar artist -> {artist: {country: }
        #[{'Megadth': {'country': 'USA', 'genre': 'thrash', }},{'Flotsam & Jetsam'...etc}]

        item = response.meta['item']
        item['similar_artists'] = []
        soup = BeautifulSoup(response.body)
        similar_artist_list = [child.text.encode('utf-8') for child in soup.find_all('td') if not child.has_attr('colspan') and not child.find_all('span')]
        #may want to do this differently
        urls = [child['href'] for child in soup.select('td a') if '#' not in child['href']]
        bands = similar_artist_list[0:len(similar_artist_list):3]
        countries = similar_artist_list[1:len(similar_artist_list):3]
        genres = similar_artist_list[2:len(similar_artist_list):3]
        for band,country,genre,url  in zip(bands,countries,genres,urls):
            if not item['similar_artists']:
                item['similar_artists'] = [
                    {band: [{'country': country},{'genre': genre},{'url': url}]}
                ]
            else:
                item['similar_artists'].append(
                    {band: [{'country': country},{'genre': genre},{'url': url}]}
                )
        related_link_url = 'http://www.metal-archives.com/link/ajax-list/type/band/id/%s' % item['id']
        yield Request(related_link_url,callback=self.parse_related_links,meta={'item':item})

    def parse_related_links(self,response):
        item = response.meta['item']
        soup = BeautifulSoup(response.body)
        item['related_links'] = {'Official_Band_Links': [],'Official_Merchandise': [],'Unofficial_Band_Links': [],'Band_Label_Links': [],\
                'Band_Tablatures': []}
        #{related links: [{'Official Band Links': [{link_desc: link1},link2,etc]},{'Official Merch': [link1,link2,..etc]}]
        #related linnks: {'Official Band Links: [{link_desc: link1},{link_desc: link2}]
        for child in soup.select('#band_links_Official a'):
            item['related_links']['Official_Band_Links'].append({child.text.encode('utf-8'): child['href']})
        for child in soup.select('#band_links_Official_merchandise a'):
            item['related_links']['Official_Merchandise'].append({child.text.encode('utf-8'): child['href']})
        for child in soup.select('#band_links_Unofficial a'):
            item['related_links']['Unofficial_Band_Links'].append({child.text.encode('utf-8'): child['href']})
        for child in soup.select('#band_links_Labls a'):
            item['related_links']['Band_Label_Links'].append({child.text.encode('utf-8'): child['href']})
        for child in soup.select('#band_links_Tablatures a'):
            item['related_links']['Band_Tablatures'].append({child.text.encode('utf-8'): child['href']})
        live_releases = 'http://www.metal-archives.com/band/discography/id/%s/tab/lives' % item['id']
        yield Request(live_releases,callback=self.parse_live_releases,meta={'item':item})

    def parse_live_releases(self,response):
        item = response.meta['item']
        soup = BeautifulSoup(response.body)
        item['releases'] = {'all_releases': [],'live_releases': [],'demo_releases': [],'misc_releases': [],'main_releases': [],'release_count': 0}

        release_info = [child.text.encode('utf-8').strip() for child in soup.select('tbody td') if '%' not in child.text.encode('utf-8') and len(child.text.encode('utf-8').strip()) != 0]
        release_names = release_info[0:len(release_info):3]
        release_types = release_info[1:len(release_info):3]
        release_years = release_info[2:len(release_info):3]
        for release_name,release_type,release_year in zip(release_names,release_types,release_years):
            item['releases']['live_releases'].append({'release_name': {release_name: {'release_type': release_type,'release_year': release_year}}})

        demo_releases = 'http://www.metal-archives.com/band/discography/id/%s/tab/demos' % item['id']
        yield Request(demo_releases,callback=self.parse_demo_releases,meta={'item':item})

    def parse_demo_releases(self,response):
        item = response.meta['item']
        soup = BeautifulSoup(response.body)

        release_info = [child.text.encode('utf-8').strip() for child in soup.select('tbody td') if '%' not in child.text.encode('utf-8') and len(child.text.encode('utf-8').strip()) != 0]
        release_names = release_info[0:len(release_info):3]
        release_types = release_info[1:len(release_info):3]
        release_years = release_info[2:len(release_info):3]
        for release_name,release_type,release_year in zip(release_names,release_types,release_years):
            item['releases']['demo_releases'].append({'release_name': {release_name: {'release_type': release_type,'release_year': release_year}}})
        misc_releases = 'http://www.metal-archives.com/band/discography/id/%s/tab/misc' % item['id']
        yield Request(misc_releases,callback=self.parse_misc_releases,meta={'item':item})

    def parse_misc_releases(self,response):
        item = response.meta['item']
        soup = BeautifulSoup(response.body)
        release_info = [child.text.encode('utf-8').strip() for child in soup.select('tbody td') if '%' not in child.text.encode('utf-8') and len(child.text.encode('utf-8').strip()) != 0]
        release_names = release_info[0:len(release_info):3]
        release_types = release_info[1:len(release_info):3]
        release_years = release_info[2:len(release_info):3]
        for release_name,release_type,release_year in zip(release_names,release_types,release_years):
            item['releases']['misc_releases'].append({'release_name': {release_name: {'release_type': release_type,'release_year': release_year}}})
        main_releases = 'http://www.metal-archives.com/band/discography/id/%s/tab/main' % item['id']
        yield Request(main_releases,callback=self.parse_main_releases,meta={'item':item})

    def parse_main_releases(self,response):
        item = response.meta['item']
        soup = BeautifulSoup(response.body)
        release_info = [child.text.encode('utf-8').strip() for child in soup.select('tbody td') if '%' not in child.text.encode('utf-8') and len(child.text.encode('utf-8').strip()) != 0]
        release_names = release_info[0:len(release_info):3]
        release_types = release_info[1:len(release_info):3]
        release_years = release_info[2:len(release_info):3]
        for release_name,release_type,release_year in zip(release_names,release_types,release_years):
            item['releases']['main_releases'].append({'release_name': {release_name: {'release_type': release_type,'release_year': release_year}}})
        #send request to all releases from here
        all_releases  = 'http://www.metal-archives.com/band/discography/id/%s/tab/all' % item['id']
        yield Request(all_releases,callback=self.parse_releases,meta={'item':item})

    def parse_releases(self,response):
    #discography: [{release name: {songs: [{track name: {length: 100, tracknum: 1,lyrics: lyrics}}]},type: demo, year: 1981,release_id: 3}
        #...album lineup: asdf, album notes: asdf}]
        item = response.meta['item']
        item['detailed_discography'] = []
        #{all_releases: [{name: name}, {type: type}, {year: year}}]
        soup = BeautifulSoup(response.body)

        release_info = [child.text.encode('utf-8').strip('\n\t') for child in soup.select('tbody td') if '%' not in child.text.encode('utf-8') and not any(c == '\n' or c == '\t' for c in child.text.encode('utf-8').strip('\n\t')) and len(child.text.encode('utf-8').strip()) != 0]
        release_urls = [child['href'] for child in soup.select('tbody td a') if '%' not in child.text.encode('utf-8') and len(child.text.encode('utf-8').strip()) != 0]
        release_names = release_info[0:len(release_info):3]
        release_types = release_info[1:len(release_info):3]
        release_years = release_info[2:len(release_info):3]

        release_count = len(release_urls)
        if release_count == 0:
            yield item
        item['releases']['release_count'] = release_count

        for release_url,release_name,release_type,release_year in zip(release_urls,release_names,release_types,release_years):
            item['releases']['all_releases'].append({'release_name': {release_name: {'release_type': release_type,'release_year': release_year}}})
            release_id = release_url.split('/')[6]
            release_dict = {release_name: {'songs': [],'type': release_type,'year': release_year,'release_id': release_id, 'album_lineup': [],'album_notes': '','length': '','lyrics_count': 0,'parsed_lyrics': 0},'parsed': 0}
            item['detailed_discography'].append(release_dict)
            release_index = item['detailed_discography'].index(release_dict)
            print 'the release index '+str(release_index)
            #full_release_name = '%s - %s' % (release_name,release_id)
            yield Request(release_url,callback=self.parse_individual_releases,meta={'item':item,'index': release_index,'release_name': release_name})

    def parse_individual_releases(self,response):
        #album_lineup: [{member: role},...]
        item = response.meta['item']
        release_index = response.meta['index']
        release_name = response.meta['release_name']
        soup = BeautifulSoup(response.body)

        duration = soup.select('strong')
        release_length = ''
        if len(duration) > 0:
            release_length = duration[0].text.encode('utf-8')
        item['detailed_discography'][release_index][release_name]['length'] = release_length
        print 'The release length..'+item['detailed_discography'][release_index][release_name]['length']
        band_members = soup.select('#album_members_lineup .lineupRow td a')
        member_roles_temp = soup.select('.lineupRow td')
        member_roles = member_roles_temp[1:len(member_roles_temp):2]
        member_roles = [''.join(re.split('\t|\n',role.text)) for role in member_roles]
        for member,role, in zip(band_members,member_roles):
            item['detailed_discography'][release_index][release_name]['album_lineup'].append({member.text.encode('utf-8'): role.encode('utf-8')})
        for notes in soup.select('#album_tabs_notes'):
            notes = ''.join(c for c in notes.text if not c in '\n\r\t')
            item['detailed_discography'][release_index][release_name]['album_notes'] = notes.encode('utf-8').strip()

        track_nums = []
        for track in soup.select('.anchor'):
            track_nums.append(int((unicode(track.next_sibling)).strip('.')))
        final_track = 0
        if len(track_nums) > 0:
            final_track = max(track_nums)

        track_count = 0
        parsed_lyrics = 0
        lyrics_count = soup.text.encode('utf-8').count("Show lyrics")
        item['detailed_discography'][release_index][release_name]['lyrics_count'] = lyrics_count
        for child in soup.find_all('tbody'):
            for track in child.select('.wrapWords'):
                track_count += 1
                track_name = track.text.encode('utf-8').strip()
                track_name = ''.join( c for c in track_name if c not in '\n\t;' )
                track_length = track.next_sibling.next_sibling.text.encode('utf-8').strip()
                song_dict = {track_name: {'number': track_count,'length': track_length,'lyrics': ''}}
                item['detailed_discography'][release_index][release_name]['songs'].append(song_dict)
                song_index = item['detailed_discography'][release_index][release_name]['songs'].index(song_dict)

                lyrics_tag = track.next_sibling.next_sibling.next_sibling.next_sibling.find_all(href=True)
                lyrics_base_url = 'http://www.metal-archives.com/release/ajax-view-lyrics/id/'
                if len(lyrics_tag) > 0:
                    parsed_lyrics += 1
                    lyrics_url_value = lyrics_tag[0].get('href')
                    lyrics_id = ''.join([char for char in lyrics_url_value if char.isdigit()])
                    lyrics_url = lyrics_base_url+lyrics_id
                    meta={'item':item,'index': release_index,'song_index': song_index,'release_name': release_name,\
                            'track_name': track_name,'parsed_lyrics': parsed_lyrics,'track_count': track_count,\
                            'final_track': final_track}
                    yield Request(lyrics_url,callback=self.parse_lyrics,meta=meta,dont_filter=True)

        if lyrics_count == 0:
            print 'Lyrics count is zero..'
            print 'The length of the discography:\t'+str(len(item['detailed_discography']))
            print 'The number of releases:\t'+str(item['releases']['release_count'])
            #if len(item['detailed_discography']) == item['releases']['release_count']:
            item['detailed_discography'][release_index]['parsed'] = 1
            parsed_count = 0
            for release in item['detailed_discography']:
                if release['parsed'] == 1:
                    parsed_count += 1
            print 'The parsed count/release count: %s\t%s'% (parsed_count,item['releases']['release_count'])
            if parsed_count == item['releases']['release_count']:
               #.text.encode('utf-8')_file = 'bands.txt'
               # all_bands = 'total_bands.txt'
               # with open.text.encode('utf-8')_file, 'a') as f:
               #     f.write(item['name']+'\n')
               # for band in total_bands:
               #     with open(all_bands, 'a') as f:
               #         f.write(band+'\n')
               #         total_bands.remove(band)
                yield item


    def parse_lyrics(self,response):
        item = response.meta['item']
        release_index = response.meta['index']
        song_index= response.meta['song_index']
        release_name = response.meta['release_name']
        track_name = response.meta['track_name']
        track_count = response.meta['track_count']
        final_track = response.meta['final_track']
        item['detailed_discography'][release_index][release_name]['parsed_lyrics'] += 1
        parsed_lyrics = item['detailed_discography'][release_index][release_name]['parsed_lyrics']
        lyrics_count = item['detailed_discography'][release_index][release_name]['lyrics_count']
        soup = BeautifulSoup(response.body)
        #lyrics = soup.text.encode('utf-8')
        lyrics = ''.join(c for c in soup.text.strip().encode('utf-8') if not c in '\r\t').replace('\n',' ')
        item['detailed_discography'][release_index][release_name]['songs'][song_index][track_name]['lyrics'] = lyrics
        #Need to figure out how to go through all releases
        print 'The length of the discography:\t'+str(len(item['detailed_discography']))
        print 'The number of releases:\t'+str(item['releases']['release_count'])
        #if len(item['detailed_discography']) == item['releases']['release_count']:
        if parsed_lyrics == lyrics_count:
            #if track_count == final_track:
            item['detailed_discography'][release_index]['parsed'] = 1
            parsed_count = 0
            for release in item['detailed_discography']:
                if release['parsed'] == 1:
                    parsed_count += 1
            print 'The parsed count/release count: %s\t%s'% (parsed_count,item['releases']['release_count'])
            if parsed_count == item['releases']['release_count']:
                #.text.encode('utf-8')_file = 'bands.txt'
                #all_bands = 'total_bands.txt'
                #with open.text.encode('utf-8')_file, 'a') as f:
                #    f.write(item['name']+'\n')
                #for band in total_bands:
                #    with open(all_bands, 'a') as f:
                #        f.write(band+'\n')
                #        total_bands.remove(band)
                yield item
