# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Destination(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = _('Destination')
        verbose_name_plural = _('Destinations')

    def __str__(self):
        return self.name

class Link(models.Model):
    TOURISM = 'TOURISM'
    HOTELS = 'HOTELS'
    BED_BREAKFEST = 'BED_BREAKFEST'
    VACATION_RENTALS = 'VACATION_RENTALS'
    VACATION_PACKAGES = 'VACATION_PACKAGES'
    FLIGHTS = 'FLIGHTS'
    RESTAURANTS = 'RESTAURANTS'
    THINGS_TO_DO = 'THINGS_TO_DO'
    TRAVEL_FOURM = 'TRAVEL_FOURM'
    TRAVEL_GUIDE = 'TRAVEL_GUIDE'
    CATEGORY_CHOICES = (
        (TOURISM, 'Tourism'),
        (HOTELS, 'Hotels'),
        (BED_BREAKFEST, 'Bed and Breakfast'),
        (VACATION_RENTALS, 'Vacation Rentals'),
        (VACATION_PACKAGES, 'Vacation Packages'),
        (FLIGHTS, 'Flights'),
        (RESTAURANTS, 'Restaurants'),
        (THINGS_TO_DO, 'Things to Do'),
        (TRAVEL_FOURM, 'Travel Forum'),
        (TRAVEL_GUIDE, 'Travel Guide'),
    )
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default=TOURISM,
    )
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE)
    url = models.URLField()

    class Meta:
        verbose_name = _('Link')
        verbose_name_plural = _('Links')

    def __str__(self):
        return self.url

class Listing(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)
    about = models.TextField(blank=True)
    link = models.ForeignKey('Link', on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    website = models.CharField(max_length=255, blank=True)
    features = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    price_from = models.CharField(max_length=255, blank=True)
    price_to = models.CharField(max_length=255, blank=True)
    lat = models.CharField(max_length=255, blank=True)
    lng = models.CharField(max_length=255, blank=True)

    about_ar = models.TextField(blank=True)
    title_ar = models.TextField(blank=True)

    class Meta:
        verbose_name = _('Listing')
        verbose_name_plural = _('Listings')

    def __str__(self):
        return self.title

class WorkingHours(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)
    day = models.CharField(max_length=125)
    time_from = models.CharField(max_length=125, blank=True)
    time_to = models.CharField(max_length=125, blank=True)

    class Meta:
        verbose_name = _('WorkingHour')
        verbose_name_plural = _('WorkingHours')

    def __str__(self):
        return self.day
