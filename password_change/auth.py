# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from django.shortcuts import render
#from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import translation
import logging
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from .forms import ChangePasswordForm
from ldap_people.models import LdapPerson
from ldap_people.models import LdapGroup
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.decorators import login_required
from .decorators import enable_user_password_change
from django.utils.translation import ugettext as _
from django.contrib import messages


@login_required
@enable_user_password_change
def password_change(request):
    context={}
    return render(request, 'password_change.html', context)

   
@login_required
@enable_user_password_change
def password_change_complete(request):
    context = {}
    user = None
    ldap_user = None
    
    if request.method != 'POST':
        logging.warning("Attempt to reset password without using post method as it should be")
        return redirect('login')
         
    password = request.POST.get('password')
    
    try:
        user = authenticate(username=request.user.username, password=password)
    except Exception as e:
        logging.error(e)

    try:
        ldap_user = LdapPerson.get_by_uid(request.user.username)
    except Exception as e:
        logging.error(e)

        
    if user is None or ldap_user is None:
        messages.warning(request, _('user_not_found'))
        logging.error('Error changing password user {}'.format(user))
        return render(request, 'password_change.html')


    if not LdapPerson.belongs_to_restricted_group(user.username):
        logging.warning("The user belongs to a group that is not allowed to change the password")
        messages.warning(request, _('user_not_valid_for_this_action'))
        return render(request, 'password_change.html')

        
    logging.warning('Activating new password for user {}'.format(user.username))

    form =  ChangePasswordForm(request.POST)
    if form.is_valid():
        try:
            new_password = form.cleaned_data['password1']

            logging.warning("changing password for ldap user ...")
            LdapPerson.change_password(user.username, password, new_password)

            logging.warning("changing password for django user ...")
            user.set_password(new_password)
            user.save()
            logout(request)
            
            return render(request, 'password_change_complete.html')
        except Exception, e:
            logging.warning("ERROR, password not changed. {}".format(e))
            return render(request, 'password_change_error.html')
    else:
        context.update({'form': form})
        logging.warning("Invalid confirm change password form, errors: %s" % form.errors)
        return render(request, 'password_change.html', context)
