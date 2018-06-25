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
        return self.name.encode('utf8')

class Link(models.Model):
    NATURE_PARKS = 'NATURE_PARKS'
    MUSEUMS = 'MUSEUMS'
    SHOPPING = 'SHOPPING'
    ZOOS_AQUARIUMS = 'ZOOS_AQUARIUMS'
    FOOD_DRINK = 'FOOD_DRINK'
    WATER_AMUSEMENT_PARKS = 'WATER_AMUSEMENT_PARKS'
    RESTAURANTS = 'RESTAURANTS'
    CATEGORY_CHOICES = (
        (NATURE_PARKS, 'Nature & Parks'),
        (MUSEUMS, 'Museums'),
        (SHOPPING, 'Shopping'),
        (ZOOS_AQUARIUMS, 'Zoos & Aquariums'),
        (FOOD_DRINK, 'Food & Drink'),
        (WATER_AMUSEMENT_PARKS, 'Water & Amusement Parks'),
        (RESTAURANTS, 'Restaurants'),
    )

    TRIPADVISOR = 'TRIPADVISOR'
    BOOKING = 'BOOKING'
    OTHER = 'OTHER'
    SOURCE_CHOICES = (
        (TRIPADVISOR, 'tripadvisor'),
        (BOOKING, 'Booking'),
        (OTHER, 'Other'),
    )

    category = models.CharField(
        max_length=200,
        choices=CATEGORY_CHOICES,
        default=NATURE_PARKS,
    )
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE)
    items_count = models.IntegerField(default=10)
    url = models.URLField()
    executed = models.BooleanField(default=False)
    source = models.CharField(
        max_length=200,
        choices=SOURCE_CHOICES,
        default=TRIPADVISOR,
    )

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
    features = models.TextField(blank=True)
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
