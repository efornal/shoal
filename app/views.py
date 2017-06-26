# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from ldap_people.models import LdapPerson
from ldap_people.models import Office
from ldap_people.models import LdapGroup
from django.shortcuts import redirect
from django.utils import translation
import logging
from django.contrib import messages
from ldap_people.forms import LdapPersonForm, FrontLdapPersonForm
from decorators import ldap_user_required
from django.conf import settings


def set_language(request, lang='es'):
    if 'lang' in request.GET:
        lang = request.GET['lang']
    translation.activate(lang)
    request.session[translation.LANGUAGE_SESSION_KEY] = lang
    logging.info("Language changed by the user to '{}'".format(lang))
    return redirect('index')


def index(request):
    context={}
    people  = LdapPerson.by_offices()
    offices = Office.telephones()

    # for person in people:
    #     logging.error(person)
    #     if person.office is not None:
    #         curr_phone = offices.get('{}'.format(person.office))
    #         if curr_phone and person.telephone_number \
    #            and person.telephone_number is not None \
    #            and person.telephone_number not in curr_phone:
    #             curr_phone = '{}, {}'.format( curr_phone,person.telephone_number)
    #         else:
    #             if person.telephone_number is not None:
    #                 curr_phone = '{}'.format( person.telephone_number)
    #             else:
    #                 curr_phone = ''
                    

        
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
    form = LdapPersonForm(instance=person)
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
                
    context={'show_extra_info':show_extra_info}
    if 'text' in request.GET:
        text = request.GET['text']
        people = LdapPerson.search(text)
        context.update({'people': people})

        if people is None:
            logging.warning ("Failed to perform text search {}".format(text))
            messages.info(request, _('search_error'))
        
    return render(request, 'search.html', context)

def search_by_office(request):
    user_groups = []
    context = {}
    show_extra_info = is_in_group_with_extra_info(request)
                
    context={'show_extra_info':show_extra_info}
    if 'text' in request.GET:
        text = request.GET['text']
        people = LdapPerson.search(text)
        context.update({'people': people})

        if people is None:
            logging.warning ("Failed to perform text search {}".format(text))
            messages.info(request, _('search_error'))
        
    return render(request, 'search.html', context)
