from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import logging
from ldap_people.models import LdapPerson
from django.utils.translation import ugettext as _


        
class ChangePasswordForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('password','password1', 'password2')
