# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from jet.admin import CompactInline
from django import forms
from django.contrib import admin
from tripadvisor.models import Destination, Link, Listing, WorkingHours
from tripadvisor.forms import DestinationForm, LinkForm
# from tripadvisor.scraping import AnalyzeScrape
from tripadvisor.scraper import TripadvisorScraper


class DestinationInline(CompactInline):
    model = Destination
    extra = 1
    show_change_link = True


class DestinationAdmin(admin.ModelAdmin):
    form = DestinationForm
    list_display = (
        'name',
    )
    search_fields = ('name', 'parent')


class LinkAdmin(admin.ModelAdmin):
    form = LinkForm
    actions = ['scrape_listing',]
    list_display = (
        'url',
        'category',
        'destination',
        'items_count',
        'source',
        'executed',
    )
    search_fields = ('destination', 'name', 'category', 'items_count', 'source', 'executed',)

    def scrape_listing(self, request, queryset):
        for obj in queryset:
            scraper = TripadvisorScraper()
            scraper.fetch_listings(obj)
            scraper.close()
        self.message_user(request, "Listing successfully scraped.")
    scrape_listing.short_description = "Scrape Listing"


class WorkingHoursInline(CompactInline):
    model = WorkingHours
    extra = 1
    show_change_link = True


class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'title_ar',
        'about',
        'about_ar',
    )
    list_editable = ('title_ar', 'about_ar',)
    list_filter = (
        'title',
        'link__category',
    )
    search_fields = ('title', 'link__category', 'url',)
    inlines = (WorkingHoursInline,)


admin.site.register(Destination, DestinationAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Listing, ListingAdmin)