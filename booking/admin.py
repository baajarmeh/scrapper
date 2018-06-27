# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from booking.forms import SourceForm
from booking.models import Source, Hotel as HotelModel
from booking.scrapper.hotel import Hotel as HotelScrapper


class SourceAdmin(admin.ModelAdmin):
    form = SourceForm
    actions = ['scrape_hotels',]
    list_display = (
        'url',
        'destination',
        'items_count',
        'executed',
    )
    search_fields = ('destination', 'name', 'items_count', 'executed',)

    def scrape_hotels(self, request, queryset):
        c = 0
        for obj in queryset:
            # if not obj.executed:
            scrapper = HotelScrapper(obj=obj)

            scrapper.fetch_hotels()
            scrapper.close()
            c += 1
        
        if c == 1:
            message_bit = "1 source was"
        else:
            message_bit = "%s source were" % c
        self.message_user(request, "%s scraped successfully." % message_bit)
    scrape_hotels.short_description = "Scrape Hotels"


class HotelAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'title_ar',
        'about',
        'about_ar',
        'features',
        'features_ar',
    )
    list_editable = ('title_ar', 'about_ar', 'features_ar')
    list_filter = ('title',)
    search_fields = ('title', 'url',)


admin.site.register(Source, SourceAdmin)
admin.site.register(HotelModel, HotelAdmin)
