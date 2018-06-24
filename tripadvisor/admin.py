# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from jet.admin import CompactInline
from django.contrib import admin
from object_actions import BaayObjectActions
from tripadvisor.models import Destination, Link, Listing, WorkingHours
from tripadvisor.scraping import AnalyzeScrape


class DestinationInline(CompactInline):
    model = Destination
    extra = 1
    show_change_link = True


class DestinationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    search_fields = ('name', 'parent')
    inlines = (DestinationInline,)


class LinkAdmin(AnalyzeScrape, BaayObjectActions, admin.ModelAdmin):
    list_display = (
        'url',
        'category',
        'destination',
        'items_count',
        'source',
        'executed',
    )
    search_fields = ('name', 'category', 'items_count', 'source', 'executed',)

    def scrape_listing(self, request, obj):
        self.index_scraping(obj, obj.url, obj.items_count)
    scrape_listing.label = "Scrape Listing"
    scrape_listing.short_description = "This will be the scraping of the listing"


class WorkingHoursInline(CompactInline):
    model = WorkingHours
    extra = 1
    show_change_link = True


class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'title_ar',
        'address',
        'link',
        'url',
    )
    list_editable = ('title_ar',)
    list_filter = (
        'title',
        'link__category',
        'address',
        'url',
    )
    search_fields = ('title', 'address', 'link__category', 'url', 'title_ar')
    inlines = (WorkingHoursInline,)


admin.site.register(Destination, DestinationAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Listing, ListingAdmin)