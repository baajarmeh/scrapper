# -*- coding: utf-8 -*-
import time
import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from tripadvisor.models import Listing, WorkingHours


class Restaurant():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.listings = []
        self.main_window = None

    def fetch_listings(self, obj):
        self.driver.get(obj.url)
        self.driver.implicitly_wait(2)
        i = 0
        elements = self.driver.find_elements_by_css_selector('.listing')
        for e in elements:
            try:
                if i < obj.items_count:
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
            self._parse_listing(obj, listing)

    def close(self):
        self.driver.close()

    def _parse_listing(self, obj, listing):
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
        
        time.sleep(5)
        self.driver.execute_script("window.scrollTo(0, 6000);")
        # self.driver.execute_script('document.querySelector(".mapContainer").scrollIntoView(true);')

        lat, lng = self._parse_location()
        website = self._parse_website()

        listing = Listing(
            url=url,
            title=title,
            about=desc,
            link=obj,
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
        
        obj.executed = True
        obj.save()
        # self.driver.close()
        self.driver.switch_to_window(self.main_window)
    
    def _parse_description(self):
        desc = self.driver.find_element_by_css_selector('div#RESTAURANT_DETAILS .additional_info:last-child .content').text
        try:
            about = self.driver.find_element_by_xpath("//*[@id='RESTAURANT_DETAILS']//*[contains(text(), 'Description')]/parent::*//[@class='content']").text

            logging.warning('last additional' + desc)
            logging.warning('xpath --find-- description' + about)
        except NoSuchElementException:
            logging.warning('last additional' + desc)
            logging.warning('xpath --not-- find description')
            about = None
        
        return about
    
    def _parse_features(self):
        try:
            features = self.driver.find_element_by_xpath("//*[@class='table_section']//*[@class='title' and contains(text(), 'Restaurant features')]/parent::*//[@class='content']").text
            logging.warning('xpath --find-- features' + features)
        except NoSuchElementException:
            logging.warning('xpath --not-- features')
            features = None

        return features
    
    def _parse_email(self):
        try:
            email = self.driver.find_element_by_xpath("//*[@id='RESTAURANT_DETAILS']//*[@class='additional_info']//*a[contains(@href, 'mailto:')]").get_attribute('href')
            logging.warning('xpath --find-- email' + email)
        except NoSuchElementException:
            logging.warning('xpath --not-- email')
            email = None
        
        return email
    
    def _parse_location(self):
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
        
        return lat, lng
    
    def _parse_website(self):
        # try to get website link
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
            else:
                website = None
        except NoSuchElementException:
            website = None
        
        return website
    
    def _parse_working_hours(self, listing):
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
