# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from ldap_people.models import LdapPerson
from django.shortcuts import redirect
from django.utils import translation
import logging
from django.contrib import messages
from ldap_people.forms import LdapPersonForm, FrontLdapPersonForm
from decorators import ldap_user_required
    
def set_language(request, lang='es'):
    if 'lang' in request.GET:
        lang = request.GET['lang']
    translation.activate(lang)
    request.session[translation.LANGUAGE_SESSION_KEY] = lang
    return redirect('index')


def index(request):
    context={}
    return render(request, 'index.html', context)


def logout_message(request):
    context={}
    return render(request, 'logout.html', context)


@login_required
@ldap_user_required
def edit(request):
    person = LdapPerson.get_by_uid(request.user)
    form = LdapPersonForm(instance=person)
    context={'form':form}
    return render(request, 'edit.html', context)


@login_required
@ldap_user_required
def save(request):
    context={}
    person = LdapPerson.get_by_uid(request.user)
    params = request.POST.copy()
    params.update({'username':request.user.username})
    params.update({'email': person.email})
    form = FrontLdapPersonForm(params,instance=person)

    if form.is_valid():
        form.instance.save()
        messages.info(request, _('changes_saved'))
    else:
        logging.warning ("Error to update ldap person {}".format(form.errors))
        context.update({'form': form})
        return render(request, 'edit.html', context)

    return redirect('edit')


def search(request):
    context={}
    if 'text' in request.GET:
        text = request.GET['text']
        people = LdapPerson.search(text)
        context.update({'people': people})

        if people is None:
            logging.warning ("Failed to perform text search {}".format(text))
            messages.info(request, _('search_error'))
        
    return render(request, 'search.html', context)
