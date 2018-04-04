# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from ldap_people.models import LdapPerson
import logging
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.conf import settings
from http_auth import basic_http_authentication


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



def validate_basic_http_authentication(view):

    def wrap(request, *args, **kwargs):
        user = basic_http_authentication(request)
        if user is None:
            logging.error("Invalid username or password")
            return HttpResponse('401 Unauthorized', status=401)
        else:
            return view(request, *args, **kwargs)
        
    return wrap



def validate_basic_http_header(view):

    def wrap(request, *args, **kwargs):
        if not 'HTTP_AUTHORIZATION' in request.META:
            logging.error("No key HTTP_AUTHORIZATION in request")
            response = HttpResponse()
            response.status_code = 401
            response['WWW-Authenticate'] = 'Basic realm=User Authentication'
            return response
        else:
            return view(request, *args, **kwargs)

    return wrap



def validate_https_request(view):

    def wrap(request, *args, **kwargs):
        if not 'REQUEST_SCHEME' in request.META or request.META['REQUEST_SCHEME'] != 'https':
            logging.error("The key REQUEST_SCHEME is not HTTPS")
            response = HttpResponse()
            response.status_code = 401
            response['WWW-Authenticate'] = 'Basic realm=User Authentication'
            return response
        else:
            return view(request, *args, **kwargs)

    return wrap
