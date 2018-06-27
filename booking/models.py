# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Source(models.Model):
    destination = models.ForeignKey('tripadvisor.Destination', on_delete=models.CASCADE)
    items_count = models.IntegerField(default=10)
    url = models.URLField()
    executed = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Source')
        verbose_name_plural = _('Sources')

    def __str__(self):
        return self.url

class Hotel(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)
    stars_count = models.IntegerField(default=0)
    about = models.TextField(blank=True, null=True)
    link = models.ForeignKey('Source', on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    price_from = models.CharField(max_length=255, blank=True, null=True)
    price_to = models.CharField(max_length=255, blank=True, null=True)
    lat = models.CharField(max_length=255, blank=True, null=True)
    lng = models.CharField(max_length=255, blank=True, null=True)

    about_ar = models.TextField(blank=True, null=True)
    title_ar = models.TextField(blank=True, null=True)
    features_ar = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('Hotel')
        verbose_name_plural = _('Hotels')

    def __str__(self):
        return self.title.encode('utf8')