# -*- coding: utf-8 -*-
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
# from urllib import urlencode, urlopen
# from urlparse import parse_qsl, urlparse
from tripadvisor.models import Listing, WorkingHours


class TripadvisorScraper():
    def __init__(self, engine='phantomjs'):
        self.host = 'https://www.tripadvisor.com'
        self.driver = webdriver.Chrome()
        self.listings = []
        self.main_window = None

    def _parse_page(self, counter, obj):
        self.driver.implicitly_wait(2)

        i = 0
        elements = self.driver.find_elements_by_css_selector('.listing')
        for e in elements:
            try:
                if i < counter:
                    listing = e.find_element_by_css_selector('.title a')
                    self.listings.append(listing)
                    i += 1
                else:
                    break
            except:
                logging.warning('Couldn\'t fetch listing.')
                pass

        self.main_window = self.driver.current_window_handle

        for listing in self.listings:
            # self.current += 1
            # logging.warning('link is :' + listing)
            if obj.category == 'RESTAURANTS':
                self._parse_restaurat_listing(obj, listing)
            else:
                self._parse_things_todo_listing(obj, listing)

    def _parse_restaurat_listing(self, obj, listing):
        url = listing.get_attribute('href')
        listing.click()
        self.driver.switch_to_window(self.driver.window_handles[-1])
        self.driver.implicitly_wait(5)

        title = self.driver.find_element_by_css_selector('h1#HEADING').text
        about = self.driver.find_element_by_css_selector('div#RESTAURANT_DETAILS .additional_info:last-child .content').text
        # desc = self.driver.find_element_by_xpath("//input[@id='passwd-id']") # //*[@id="RESTAURANT_DETAILS"]//*[@class="additional_info"][last()]/*[@class="content"]:not([ul])
        address = self.driver.find_element_by_css_selector('.headerBL .blEntry.address').text
        # img_map = self.driver.find_element_by_css_selector('.staticMap img').get_attribute('src')
        phone = self.driver.find_element_by_css_selector('.blEntry.phone').text
        
        time.sleep(5)
        self.driver.execute_script("window.scrollTo(0, 6000);")
        # self.driver.execute_script('document.querySelector(".mapContainer").scrollIntoView(true);')

        element = self.driver.find_element_by_css_selector(".dynamicMap")
        self.driver.execute_script("return arguments[0].scrollIntoView();", element)
        self.driver.implicitly_wait(2)

        try:
            loc = self.driver.find_element_by_css_selector('.mapContainer')
            lat = loc.get_attribute('data-lat')
            lng = loc.get_attribute('data-lng')
        except NoSuchElementException:
            lat = None
            lng = None

        listing = Listing(
            url=self.host + url,
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

        hours = self.driver.find_elements_by_css_selector('div#RESTAURANT_DETAILS .row .hours.content .detail')
        i = 0
        while i < len(hours):
            day = hours[i].find_element_by_css_selector('span.day').text

            for hours_range in hours[i].find_elements_by_css_selector('span.hours .hoursRange'):
                between = str(hours_range.text).split('-')

                working = WorkingHours(
                    listing=listing,
                    day=day,
                    time_from=between[0],
                    time_to=between[1],
                )
                working.save()
            i += 1

        # obj.executed = True
        # obj.save()
        self.driver.close()
        self.driver.switch_to_window(self.main_window)

    def _parse_things_todo_listing(self, obj, url=''):
        self.driver.get(url)
        # self.driver.implicitly_wait(2)

        title = self.driver.find_element_by_css_selector('h1#HEADING').text
        about = self.driver.find_element_by_css_selector('.location_btf_wrap .description .text').text
        address = self.driver.find_element_by_css_selector('.headerBL .blEntry.address').text
        # img_map = self.driver.find_element_by_css_selector('.staticMap img').get_attribute('src')
        phone = self.driver.find_element_by_css_selector('.blEntry.phone').text

        try:
            map_loc = self.driver.find_element_by_css_selector('.dynamicMap')
            actions = ActionChains(self.driver)
            actions.move_to_element(map_loc).perform()

            time.sleep(2)

            loc = self.driver.find_element_by_css_selector('.dynamicMap .mapContainer')
            lat = loc.get_attribute('data-lat')
            lng = loc.get_attribute('data-lng')
        except NoSuchElementException:
            lat = None
            lng = None
        
        # query_pairs = dict(parse_qsl(urlparse(img_map).query))
        # center_loc = query_pairs['center'].split(',')

        # price_from = 
        # price_to = 
        

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

        hours = self.driver.find_elements_by_css_selector('div#RESTAURANT_DETAILS .row .hours.content .detail')
        i = 0
        while i < len(hours):
            day = hours[i].find_element_by_css_selector('span.day').text

            for hours_range in hours[i].find_elements_by_css_selector('span.hours .hoursRange'):
                between = hours_range.text().split('-')

                working = WorkingHours(
                    listing=listing,
                    day=day,
                    time_from=between[0],
                    time_to=between[1],
                )
                working.save()
            i += 1

        # obj.executed = True
        # obj.save()
        # self.driver.close()

    def fetch_listings(self, obj):
        self.driver.get(obj.url)
        # self.driver.implicitly_wait(5)

        # time.sleep(5)
        self._parse_page(obj.items_count, obj)

    def close(self):
        self.driver.close()

