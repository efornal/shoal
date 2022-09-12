# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.forms import ModelForm
from ldap_people.models import LdapPerson
from ldap_people.models import LdapOffice
from ldap_people.models import LdapGroup
from ldap_people.models import Office
from django.utils.translation import ugettext as _
from django.utils import translation
from django.contrib import messages
import logging
from django.conf import settings
#from importlib import reload
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LdapPersonAdminForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        max_length=200,
        label=_('Username'))
    name = forms.CharField(
        max_length=200,
        required=True,
        label=_('Name'))
    surname = forms.CharField(
        max_length=200,
        required=True,
        label=_('Surname'))
    email = forms.EmailField(
        max_length=200,
        required=True,
        label=_('Email'))
    alternative_email = forms.EmailField(
        max_length=200,
        required=False,
        label=_('Alternative_email'))
    office = forms.ChoiceField(
        choices=LdapOffice.choices_with_blank(),
        required=False,
        label=_('Office'))
    other_office = forms.CharField(
        max_length=200,
        required=False,
        label=_('Other_office'))
    group_id = forms.ChoiceField(
        choices=[(group.group_id, group.name) for group in LdapGroup.all()],
        required=False,
        label=_('Main_group'))
    groups_id = forms.MultipleChoiceField(
        widget=forms.SelectMultiple,
        choices=[(group.group_id, group.name) for group in LdapGroup.all()],
        required=False,
        label=_('Secondary_groups'))
    document_number = forms.CharField(
        max_length=200,
        required=False,
        label=_('Document_number'))
    type_document_number = forms.CharField(
        max_length=200,
        required=False,
        label=_('Type_document_number'))
    telephone_number = forms.CharField(
        max_length=200,
        required=False,
        label=_('Telephone_number'))
    home_telephone_number = forms.CharField(
        max_length=200,
        required=False,
        label=_('Home_telephone_number'))
    floor = forms.CharField(
        max_length=200,
        required=False,
        label=_('Floor'))
    area = forms.CharField(
        max_length=200,
        required=False,
        label=_('Area'))
    position = forms.CharField(
        max_length=200,
        required=False,
        label=_('Position'))
    host_name = forms.CharField(
        max_length=200,
        required=False,
        label=_('Host_name'))

    class Meta:
        model = LdapPerson
        fields = ('username','name','surname','email','alternative_email', \
                  'document_number','type_document_number', 'host_name', \
                  'office','telephone_number','home_telephone_number','other_office')

    def __init__(self, *args, **kwargs):
        super(LdapPersonAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            member_groups = [str(x.group_id) for x in LdapGroup.groups_by_uid(self.instance.username)]
            self.initial['groups_id'] = member_groups

       
def validate_telephone_number(val):
    pattern = r'^(^(int )?\d{1,3})(((,|/)\d{1,3}){0,10})$'
    return re.match(pattern, val)

class FrontLdapPersonForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        max_length=200,
        label=_('Username'))
    name = forms.CharField(
        max_length=200,
        required=False,
        label=_('Name'))
    surname = forms.CharField(
        max_length=200,
        required=False,
        label=_('Surname'))
    office = forms.CharField(
        max_length=200,
        required=False,
        label=_('Office'))
    email = forms.EmailField(
        max_length=200,
        required=True,
        label=_('Email'))
    alternative_email = forms.EmailField(
        max_length=200,
        required=False,
        label=_('Alternative_email'))
    document_number = forms.CharField(
        max_length=200,
        required=False,
        label=_('Document_number'))
    type_document_number = forms.CharField(
        max_length=200,
        required=False,
        label=_('type_document_number'))
    telephone_number = forms.CharField(
        max_length=200,
        required=False,
        label=_('telephone_number'))
    home_telephone_number = forms.CharField(
        max_length=200,
        required=False,
        label=_('home_telephone_number'))

    class Meta:
        model = LdapPerson
        fields = ('username','name','surname','email','alternative_email',
                  'document_number','type_document_number','office',
                  'telephone_number','home_telephone_number')
        
    def clean(self):
        ldap_person = LdapPerson.get_by_uid(self.cleaned_data.get('username'))

        if not ldap_person.email:
            self.add_error('email' , _('person_without_email') )

        if self.cleaned_data.get('email') != ldap_person.email:
            self.add_error('email' , _('person_without_institutional_email') )

            
    def clean_telephone_number(self):
        telephone_number = self.cleaned_data.get('telephone_number')
        if not validate_telephone_number(telephone_number):
            logging.warning('invalid telephone number format')
            self.add_error('telephone_number' , _('invalid_format'))
        return self.cleaned_data.get('telephone_number')

    
    def clean_home_telephone_number(self):
        if 'home_telephone_number' in self.cleaned_data and \
           self.cleaned_data.get('home_telephone_number'):
            telephone_number = self.cleaned_data.get('home_telephone_number')
            if not validate_telephone_number(telephone_number):
                logging.warning('invalid home telephone number format')
                self.add_error('home_telephone_number' , _('invalid_format'))
        return self.cleaned_data.get('home_telephone_number')
    

        
class AdminChangePasswordForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('password2','password1',)

    # def clean(self):
    #     if LdapPerson.belongs_to_restricted_group(self.cleaned_data.get('username')):
    #         logging.warning("The user belongs to a group that is " \
    #                         " not allowed to change the password")
    #         self.add_error('username', _('user_not_valid_for_this_action'))



class ChangeHostNameForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        max_length=200,
        label=_('Username'))
    host_name = forms.CharField(
        max_length=200,
        required=True,
        label=_('Host_name'))
    info = forms.CharField(
        max_length=500,
        required=True,
        label=_('Info'))

    class Meta:
        model = LdapPerson
        fields = ('username', 'host_name', 'info')


