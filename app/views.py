# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from ldap_people.models import LdapPerson
from ldap_people.models import LdapOffice
from ldap_people.models import Office
from ldap_people.models import LdapGroup
from django.shortcuts import redirect
from django.utils import translation
import logging
from django.contrib import messages
from ldap_people.forms import FrontLdapPersonForm
from ldap_people.forms import ChangeHostNameForm
from app.decorators import ldap_user_required
from django.conf import settings
from django.http import HttpResponse
from decorators import validate_basic_http_header
from decorators import validate_basic_http_authentication
from decorators import validate_https_request

def set_language(request, lang='es'):
    if 'lang' in request.GET:
        lang = request.GET['lang']
    translation.activate(lang)
    request.session[translation.LANGUAGE_SESSION_KEY] = lang
    logging.info("Language changed by the user to '{}'".format(lang))
    return redirect('index')


def index(request):
    context={}
    offices = LdapOffice.telephones()
    context.update({'offices': offices})

    if 'welcome message showed' in request.session:
        request.session['welcome_message_showed'] = True
        context.update({'show_welcome_message':True})
        
    return render(request, 'index.html', context)


def logout_message(request):
    context={}
    return render(request, 'logout.html', context)


@login_required
@ldap_user_required
def edit(request):
    person = LdapPerson.get_by_uid(request.user)
    form = FrontLdapPersonForm(instance=person)
    context={'form':form}
    return render(request, 'edit.html', context)


@login_required
@ldap_user_required
def save(request):
    context={}
    person = LdapPerson.get_by_uid(request.user)
    params = request.POST.copy()
    params.update({'username':request.user.username,
                   'email': person.email,
                   'name': person.name,
                   'surname': person.surname,
                   'document_number': person.document_number,
                   'type_document_number': person.type_document_number,
                   'office': person.office})
    form = FrontLdapPersonForm(params,instance=person)
    
    if form.is_valid():
        form.instance.save()
        messages.info(request, _('changes_saved'))
    else:
        logging.warning ("Error to update ldap person {}".format(form.errors))
        context.update({'form': form})
        return render(request, 'edit.html', context)

    return redirect('edit')



def is_in_group_with_extra_info(request):
    """
    Indicates whether the registered user belongs to an ldap group 
    that allows the display of extra information
    """
    show_extra_info = False
    try:
        if request.user.is_authenticated:
            user_groups = LdapGroup.groups_by_uid(request.user)
            valid_user_groups = []
            if hasattr(settings, 'GROUPS_EXTRA_INFORMATION_SEARCH') and \
               len(settings.GROUPS_EXTRA_INFORMATION_SEARCH) > 0:
                valid_user_groups = settings.GROUPS_EXTRA_INFORMATION_SEARCH
                for user_group in user_groups:
                    if user_group.name in valid_user_groups:
                        show_extra_info = True
    except Exception as e:
        logging.error(e)

    return show_extra_info


def search(request):
    user_groups = []
    context = {}
    show_extra_info = is_in_group_with_extra_info(request)
    text = None
    context={'show_extra_info':show_extra_info}

    if 'text' in request.GET:
        text = request.GET['text']

    if not text is None:
        filter_groups = getattr(settings, "LDAP_FILTER_MEMBERS_OUT_OF_GROUPS", [])
        people = LdapPerson.search(text)
        people = LdapPerson.filter_members_out_of_groups(people,filter_groups)
        context.update({'people': people})

        if people is None:
            logging.warning ("Failed to perform text search {}".format(text))
            messages.info(request, _('search_error'))
        
    return render(request, 'search.html', context)




def search_by_office(request, office):
    user_groups = []
    context = {}
    show_extra_info = is_in_group_with_extra_info(request)
    context={'show_extra_info':show_extra_info}
    if office is not None:
        filter_groups = getattr(settings, "LDAP_FILTER_MEMBERS_OUT_OF_GROUPS", [])
        people = LdapPerson.search_by_office(office)
        people = LdapPerson.filter_members_out_of_groups(people,filter_groups)
        context.update({'people': people})

        if people is None:
            logging.warning ("Failed to perform text search {}".format(office))
            messages.info(request, _('search_error'))
        
    return render(request, 'search.html', context)


@validate_basic_http_authentication
@validate_https_request
def api_register_host(request,user,host):
    
    logging.warning("registering host access {} for user {}".format(host,user))
    params = {'username': user,'host_name': host}
    form = ChangeHostNameForm(params)
    try:
        if form.is_valid():
            form.instance.save()
            logging.warning("Access to host {} per user {} registered.".format(host,user))
            return HttpResponse('200 Successfully registered access', status=200)
        else:
            logging.error("Invalid hostname change form: {}".format(form.errors))
    except Exception as e:
        logging.error(e)

    return HttpResponse('500 Internal Server Error', status=500)

