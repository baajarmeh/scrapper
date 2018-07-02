from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from tripadvisor.models import Destination


class CountryListFilter(admin.SimpleListFilter):
    title = 'Country'
    parameter_name = 'country_id'
    related_filter_parameter = 'link__destination__parent__id__exact'

    def lookups(self, request, model_admin):
        list_of_destinations = []
        queryset = Destination.objects.order_by('name').filter(parent__isnull=True)
        for des in queryset:
            list_of_destinations.append(
                (str(des.id), des.name)
            )
        return sorted(list_of_destinations, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(link__destination__parent__id=self.value())
        return queryset
