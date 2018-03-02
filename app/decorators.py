# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from ldap_people.models import LdapPerson
import logging
from django.contrib import messages
from django.utils.translation import ugettext as _


def ldap_user_required(view):
    def wrap(request, *args, **kwargs):
        person = LdapPerson.get_by_uid(request.user.username)
        if person is None or person.username != request.user.username:
            logging.error("Could not validate ldap user")
            messages.warning(request, _('person_was_not_found'))
            return redirect('index')
        else:
            return view(request, *args, **kwargs)
    return wrap
