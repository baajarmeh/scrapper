# -*- coding: utf-8 -*-

from django import forms
from tripadvisor.models import Destination
from booking.models import Source


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        exclude = ['executed']

    def __init__(self, *args, **kwargs):
        super(SourceForm, self).__init__(*args, **kwargs)
        self.fields['destination'].queryset = Destination.objects.filter(parent__isnull=False)
