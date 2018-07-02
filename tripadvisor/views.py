# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _


def _error(request, code, message, template_name='error.html'):
    return render(request, template_name, {'code': code, 'message': message})

def page_not_found(request):
    return _error(request, 404, _('Page not found'))

def server_error(request):
    return _error(request, 500, _('Server error'))

def permission_denied(request):
    return _error(request, 403, _('Permission denied'))

def bad_request(request):
    return _error(request, 400, _('Bad request'))
