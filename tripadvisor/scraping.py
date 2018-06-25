# -*- coding: utf-8 -*-

from urlparse import parse_qsl, urlparse
from bs4 import BeautifulSoup
from tripadvisor.models import Listing, WorkingHours
try:
    import requests
except ImportError:
    pass

class AnalyzeScrape(object):
    host = 'https://www.tripadvisor.com'

    def index_scraping(self, obj, url, count):
        print("analyze index page %s" % (url))
        page = requests.get(url)
        bs = BeautifulSoup(page.text, 'html.parser')

        items = []
        i = 0
        for item in bs.select('.listItem .listing_title a'):
            if i < count:
                items.append(self.host + item.get('href'))
                i += 1
            else:
                break
        
        for link in items:
            self.listing_scraping(obj, link)
    
    def listing_scraping(self, obj, url):
        page = requests.get(url)
        bs = BeautifulSoup(page.text, 'html.parser')

        title = bs.select('h1#HEADING')[0].get_text()
        about = bs.select('.location_btf_wrap .description .text')[0].get_text()
        address = bs.select('.headerBL .blEntry.address')[0].get_text()
        img_map = bs.select('.staticMap img')[0]
        phone = bs.select('.blEntry.phone span:last-child')[0].get_text()
        
        img_src = img_map.get('src')
        query_pairs = dict(parse_qsl(urlparse(img_src).query))
        center_loc = query_pairs['center'].split(',')

        # price_from = 
        # price_to = 
        lat = center_loc[0]
        lng = center_loc[1]

        listing = Listing(
            url=url,
            title=title,
            about=about,
            link=obj,
            address=address,
            phone=phone,
            # website=website,
            # features=features,
            # email=email,
            # price_from=price_from,
            # price_to=price_to,
            lat=lat,
            lng=lng
        )
        listing.save()

        hours = bs.select('div#RESTAURANT_DETAILS .row .hours.content .detail')
        i = 0
        while i < len(hours):
            day = hours[i].select('span.day')[0].get_text()
            between = hours[i].select('span.hours .hoursRange')[0].get_text().split(' - ')

            working = WorkingHours(
                listing=listing,
                day=day,
                time_from=between[0],
                time_to=between[1],
            )
            working.save()
            i += 1
