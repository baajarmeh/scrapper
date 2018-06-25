# -*- coding: utf-8 -*-

from django import forms
from tripadvisor.models import Destination, Link


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DestinationForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Destination.objects.filter(parent__isnull=True)


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        exclude = ['executed']

    def __init__(self, *args, **kwargs):
        super(LinkForm, self).__init__(*args, **kwargs)
        self.fields['destination'].queryset = Destination.objects.filter(parent__isnull=False)
