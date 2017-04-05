# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from .models import LdapPerson
from django.shortcuts import redirect
from django.utils import translation
import logging
from django.contrib import messages


def set_language(request, lang='es'):
    if 'lang' in request.GET:
        lang = request.GET['lang']
    translation.activate(lang)
    request.session[translation.LANGUAGE_SESSION_KEY] = lang
    return redirect('index')


def index(request):
    context={}
    return render(request, 'index.html', context)


def search(request):
    context={}
    if 'text' in request.GET:
        text = request.GET['text']
        people = LdapPerson.search(text)
        if people is None:
            logging.warning ("Error al realizar la búsqueda del texto {}".format(text))
            messages.warning(request, _('search_error'))
            
        context.update({'people': people})
        
    return render(request, 'search.html', context)
