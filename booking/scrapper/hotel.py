# -*- coding: utf-8 -*-
import time
import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from urlparse import parse_qsl, urlparse
from booking.models import Hotel as HotelModel


class Hotel():
    def __init__(self, obj):
        self.driver = webdriver.Chrome()
        self.hotels = []
        self.obj = obj
        self.main_window = None

    def _fetch_page(self, page=1):
        elements = self.driver.find_elements_by_css_selector('#hotellist_inner .sr_item.sr_property_block')
        i = page + len(elements) if page > 1 else 1
        for e in elements:
            try:
                if i <= self.obj.items_count:
                    hotel = e.find_element_by_css_selector('.sr_item_content a.hotel_name_link')
                    self.hotels.append(hotel)
                    i += 1
                else:
                    break
            except:
                logging.warning('Couldn\'t fetch hotel.')
                pass

        self.main_window = self.driver.current_window_handle

        for hotel in self.hotels:
            self._parse_hotel(hotel)
    
    def fetch_hotels(self):
        self.driver.get(self.obj.url)
        self.driver.implicitly_wait(2)
        elements = self.driver.find_elements_by_css_selector('#hotellist_inner .sr_item.sr_property_block')

        if (len(elements) >= self.obj.items_count):
            self._fetch_page(1)
        else:
            page_count = ((self.obj.items_count - 1) // len(elements)) + 1
            for p in range(1, page_count):
                if p > 1:
                    try:
                        self.driver.find_elements_by_xpath("//*[@class='results-paging']//*a[text()='"+ p +"') and @class='sr_pagination_link']").click()
                        self.driver.implicitly_wait(2)
                    except:
                        break
                self._fetch_page(p)

    def close(self):
        self.driver.close()

    def _parse_hotel(self, hotel):
        hotel.click()
        self.driver.switch_to_window(self.driver.window_handles[-1])
        self.driver.implicitly_wait(5)

        url = self.driver.current_url.split('?')[0]
        title = self.driver.find_element_by_css_selector('#wrap-hotelpage-top h2#hp_hotel_name').text
        stars = self._parse_stars_count()
        address = self.driver.find_element_by_css_selector('#wrap-hotelpage-top span.hp_address_subtitle').text
        desc = self._parse_description()
        features = self._parse_features()
        lat, lng = self._parse_location()

        hotel = HotelModel(
            url=url,
            title=title,
            stars_count=stars,
            about=desc,
            link=self.obj,
            address=address,
            features=features,
            lat=lat,
            lng=lng
        )
        hotel.save()
        
        self.obj.executed = True
        self.obj.save()
        self.driver.close()
        self.driver.switch_to_window(self.main_window)
    
    def _parse_stars_count(self):
        try:
            stars_class = self.driver.find_element_by_css_selector('#wrap-hotelpage-top span.hp__hotel_ratings__stars svg.bk-icon').get_attribute('class')
            if 'stars_1' in stars_class:
                stars = 1
            elif 'stars_2' in stars_class:
                stars = 2
            elif 'stars_3' in stars_class:
                stars = 3
            elif 'stars_4' in stars_class:
                stars = 4
            elif 'stars_5' in stars_class:
                stars = 5
            else:
                stars = 0
            return stars
        except:
            return 0

    def _parse_description(self):
        return self.driver.find_element_by_css_selector('.hp-description #summary').text
    
    def _parse_features(self):
        try:
            facilities = self.driver.find_elements_by_css_selector('.hp-description .important_facility')
            features = []
            for f in facilities:
                features.append(f.text)

            return ', '.join(features)
        except:
            return None
    
    def _parse_location(self):
        try:
            style = self.driver.find_element_by_css_selector("a.map_static_zoom.show_map").get_attribute('style').split('url(')[1]
            link = style.split(') center')[0]

            query_pairs = dict(parse_qsl(urlparse(link).query))
            center_loc = query_pairs['center'].split(',')
            lat = center_loc[0]
            lng = center_loc[1]
            return lat, lng
        except:
            return None, None
