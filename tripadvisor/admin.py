# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from jet.admin import CompactInline
from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.forms import Textarea, TextInput
from django.db import models
from tripadvisor.models import Destination, Link, Listing, WorkingHours, Photo
from tripadvisor.forms import DestinationForm, LinkForm
from tripadvisor.filters import CountryListFilter
from tripadvisor.scrapper.restaurant import Restaurant
from tripadvisor.scrapper.things_todo import ThingsTodo
from sorl.thumbnail.admin import AdminImageMixin


class DestinationInline(CompactInline):
    model = Destination
    extra = 1
    show_change_link = True


class DestinationAdmin(admin.ModelAdmin):
    form = DestinationForm
    list_display = ('name',)
    search_fields = ('name', 'parent')


class LinkAdmin(admin.ModelAdmin):
    form = LinkForm
    actions = ['scrape_listing',]
    list_display = ('url', 'category', 'destination', 'items_count', 'executed',)
    search_fields = ('destination', 'name', 'category', 'items_count', 'executed',)

    def scrape_listing(self, request, queryset):
        c = 0
        for obj in queryset:
            # if not obj.executed:
            if obj.category == 'RESTAURANTS':
                scrapper = Restaurant(obj=obj)
            else:
                scrapper = ThingsTodo(obj=obj)

            scrapper.fetch_listings()
            scrapper.close()
            c += 1
        
        if c == 1:
            message_bit = "1 link was"
        else:
            message_bit = "%s link were" % c
        self.message_user(request, "%s scraped successfully." % message_bit)
    scrape_listing.short_description = "Scrape Listing"


class PhotoInline(AdminImageMixin, GenericTabularInline):
    model = Photo
    extra = 1


class WorkingHoursInline(CompactInline):
    model = WorkingHours
    extra = 1
    show_change_link = True


class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_ar', 'about', 'about_ar', 'features', 'features_ar',)
    list_editable = ('title_ar', 'about_ar', 'features_ar')
    list_filter = (CountryListFilter, 'link__category',)
    search_fields = (CountryListFilter, 'link__category', 'title',)
    inlines = (PhotoInline, WorkingHoursInline,)

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 8, 'cols': 35})},
    }


admin.site.register(Destination, DestinationAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Listing, ListingAdmin)
