# -*- coding: utf-8 -*-

from urlparse import parse_qsl, urlparse
from bs4 import BeautifulSoup
from tripadvisor.models import Listing, WorkingHours
import requests


class AnalyzeScrape(object):
    host = 'https://www.tripadvisor.com'

    def index_scraping(self, obj, url, count):
        print("analyze index page %s on %s" % (url, obj))
        page = requests.get(url)
        bs = BeautifulSoup(page.text, 'html.parser')

        items = []
        i = 0
        for item in bs.select('.listing .shortSellDetails a'):
            if i < count:
                items.append(self.host + item.get('href'))
                i += 1
            else:
                break
        
        for link in items:
            if obj.category == 'RESTAURANTS':
                self.restaurats_scraping(obj, link)
            else:
                self.things_todo_scraping(obj, link)
    
    def things_todo_scraping(self, obj, url):
        print("analyze listing page %s on %s" % (url, obj))

        page = requests.get(url)
        bs = BeautifulSoup(page.text, 'html.parser')

        title = bs.select('h1#HEADING')[0].get_text()
        about = bs.select('div#RESTAURANT_DETAILS .additional_info .content')[0].get_text()
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

            for hours_range in hours[i].select('span.hours .hoursRange'):
                between = hours_range.get_text().split(' - ')

                working = WorkingHours(
                    listing=listing,
                    day=day,
                    time_from=between[0],
                    time_to=between[1],
                )
                working.save()
            # between = hours[i].select('span.hours .hoursRange')[0].get_text().split(' - ')
            i += 1

        # obj.executed = True
        # obj.save()

    def restaurats_scraping(self, obj, url):
        print("analyze listing page %s on %s" % (url, obj))

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

            for hours_range in hours[i].select('span.hours .hoursRange'):
                between = hours_range.get_text().split(' - ')

                working = WorkingHours(
                    listing=listing,
                    day=day,
                    time_from=between[0],
                    time_to=between[1],
                )
                working.save()
            # between = hours[i].select('span.hours .hoursRange')[0].get_text().split(' - ')
            i += 1

        # obj.executed = True
        # obj.save()
