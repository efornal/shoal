# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.utils import translation
import logging

class ForceLangMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        
    def __call__(self, request):
        if not translation.LANGUAGE_SESSION_KEY in request.session \
           or not request.session[translation.LANGUAGE_SESSION_KEY] \
           and settings.LANGUAGE_CODE:
            translation.activate(settings.LANGUAGE_CODE)
            request.session[translation.LANGUAGE_SESSION_KEY] = settings.LANGUAGE_CODE
            logging.info("Activated default lang '{}'".format(settings.LANGUAGE_CODE))
        response = self.get_response(request)
        return response
            
