# -*- coding: utf-8 -*-
import time
import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from tripadvisor.models import Listing, WorkingHours


class Restaurant():
    def __init__(self, obj):
        self.driver = webdriver.Chrome()
        self.listings = []
        self.obj = obj
        self.main_window = None

    def _fetch_page(self, page=1):
        elements = self.driver.find_elements_by_css_selector('#EATERY_LIST_CONTENTS .listing')
        i = page + len(elements) if page > 1 else 1
        for e in elements:
            try:
                if i <= self.obj.items_count:
                    l = e.find_element_by_css_selector('.title a')
                    self.listings.append(l)
                    i += 1
                else:
                    break
            except:
                logging.warning('Couldn\'t fetch hotel.')
                pass

        self.main_window = self.driver.current_window_handle

        for listing in self.listings:
            self._parse_listing(listing)
    
    def fetch_listings(self):
        self.driver.get(self.obj.url)
        self.driver.implicitly_wait(2)
        elements = self.driver.find_elements_by_css_selector('#EATERY_LIST_CONTENTS .listing')

        if (len(elements) >= self.obj.items_count):
            self._fetch_page(1)
        else:
            page_count = ((self.obj.items_count - 1) // len(elements)) + 1
            for p in range(1, page_count):
                if p > 1:
                    try:
                        self.driver.find_elements_by_xpath("//*[@class='pageNumbers']//*a[text()='"+ p +"') and @class='pageNum']").click()
                        self.driver.implicitly_wait(2)
                    except:
                        break
                self._fetch_page(p)

    def close(self):
        self.driver.close()

    def _parse_listing(self, listing):
        # url = listing.get_attribute('href')
        listing.click()
        self.driver.switch_to_window(self.driver.window_handles[-1])
        self.driver.implicitly_wait(5)

        url = self.driver.current_url
        title = self.driver.find_element_by_css_selector('h1#HEADING').text
        address = self.driver.find_element_by_css_selector('.headerBL .blEntry.address').text
        phone = self.driver.find_element_by_css_selector('.blEntry.phone').text

        desc = self._parse_description()
        features = self._parse_features()
        email = self._parse_email()
        
        time.sleep(3)
        self.driver.execute_script("window.scrollTo(0, 6000);")
        # self.driver.execute_script('document.querySelector(".mapContainer").scrollIntoView(true);')

        lat, lng = self._parse_location()
        website = self._parse_website()

        listing = Listing(
            url=url,
            title=title,
            about=desc,
            link=self.obj,
            address=address,
            phone=phone,
            website=website,
            features=features,
            email=email,
            # price_from=price_from,
            # price_to=price_to,
            lat=lat,
            lng=lng
        )
        listing.save()
        self._parse_working_hours(listing)
        
        self.obj.executed = True
        self.obj.save()
        self.driver.close()
        self.driver.switch_to_window(self.main_window)
    
    def _parse_description(self):
        about = None
        try:
            about_el = self.driver.find_element_by_xpath("//*[@id='RESTAURANT_DETAILS']//*[@class='title' and contains(text(), 'Description')]")
            about = about_el.find_element_by_xpath('..').find_element_by_css_selector('.content').text
            logging.warning('xpath --find-- description' + about)
        except:
            pass
        
        return about
    
    def _parse_features(self):
        features = None
        try:
            features_el = self.driver.find_element_by_xpath("//*[@id='RESTAURANT_DETAILS']//*[@class='title' and contains(text(), 'Restaurant features')]")
            features = features_el.find_element_by_xpath('..').find_element_by_css_selector('.content').text
            logging.warning('xpath --find-- features' + features)
        except:
            pass

        return features
    
    def _parse_email(self):
        email = None
        try:
            email = self.driver.find_element_by_xpath("//*[@id='RESTAURANT_DETAILS']//*[@class='additional_info']//*a[contains(@href, 'mailto:')]").get_attribute('href')
            logging.warning('xpath --find-- email' + email)
        except:
            pass
        
        return email
    
    def _parse_location(self):
        try:
            element = self.driver.find_element_by_css_selector(".dynamicMap")
            self.driver.execute_script("return arguments[0].scrollIntoView();", element)
            self.driver.implicitly_wait(2)
        except:
            pass

        try:
            loc = self.driver.find_element_by_css_selector('.mapContainer')
            lat = loc.get_attribute('data-lat')
            lng = loc.get_attribute('data-lng')
        except:
            lat = None
            lng = None
        
        return lat, lng
    
    def _parse_website(self):
        # try to get website link
        website = None
        try:
            ahref = self.driver.find_element_by_css_selector('.blEntry.website')
            # in case website exist open window for extract url
            if ahref.get_attribute('data-ahref'):
                current_listing = self.driver.current_window_handle
                ahref.click()
                self.driver.switch_to_window(self.driver.window_handles[-1])
                website = self.driver.current_url
                self.driver.close()
                self.driver.switch_to_window(current_listing)
        except:
            pass
        
        return website
    
    def _parse_working_hours(self, listing):
        try:
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
        except:
            pass
