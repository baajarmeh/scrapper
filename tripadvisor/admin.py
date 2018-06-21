# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from jet.admin import CompactInline
from django.contrib import admin
from tripadvisor.models import Destination, Link, Listing, WorkingHours


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


class LinkAdmin(admin.ModelAdmin):
    list_display = (
        'url',
        'category',
        'destination',
    )
    search_fields = ('name', 'category',)


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