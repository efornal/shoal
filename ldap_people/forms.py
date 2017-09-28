# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.forms import ModelForm
from ldap_people.models import LdapPerson
from ldap_people.models import LdapOffice
from ldap_people.models import Office
from django.utils.translation import ugettext as _
from django.utils import translation
from django.contrib import messages
import logging
from django.conf import settings
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re

class LdapPersonForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        max_length=200)
    name = forms.CharField(
        max_length=200,
        required=True,
        label=_('name'))
    person_id = forms.CharField(
        max_length=200,
        required=False)
    surname = forms.CharField(
        max_length=200,
        required=True)
    fullname = forms.CharField(
        max_length=200,
        required=False)
    email = forms.EmailField(
        max_length=200,
        required=True)
    alternative_email = forms.EmailField(
        max_length=200,
        required=False)
    office = forms.ChoiceField(
        choices=[(office.name, office.name) for office in LdapOffice.all()],
        required=True,
        label=_('office'))
    other_office = forms.CharField(
        max_length=200,
        required=False,
        label=_('other_office'))
    group_id = forms.CharField(
        max_length=200,
        required=False)
    document_number = forms.CharField(
        max_length=200,
        required=False)
    type_document_number = forms.CharField(
        max_length=200,
        required=False)
    telephone_number = forms.CharField(
        max_length=200,
        required=False)
    home_telephone_number = forms.CharField(
        max_length=200,
        required=False)
    floor = forms.CharField(
        max_length=200,
        required=False)
    area = forms.CharField(
        max_length=200,
        required=False)
    position = forms.CharField(
        max_length=200,
        required=False)
    host_name = forms.CharField(
        max_length=200,
        required=False)

    class Meta:
        model = LdapPerson
        fields = ('username','name','surname','email','alternative_email',
                  'document_number','type_document_number', 'host_name', \
                  'office','telephone_number','home_telephone_number','other_office')

        
def validate_telephone_number(val):
    pattern = r'^\+?(\d{3,4})?(\s)?(\d{3,15})?(\s)?(int\s\d{1,3})?$'
    return re.match(pattern, val)

class FrontLdapPersonForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        max_length=200)
    name = forms.CharField(
        max_length=200,
        required=False,
        label=_('name'))
    surname = forms.CharField(
        max_length=200,
        required=False)
    office = forms.CharField(
        max_length=200,
        required=False,
        label=_('office'))
    email = forms.EmailField(
        max_length=200,
        required=True)
    alternative_email = forms.EmailField(
        max_length=200,
        required=False)
    document_number = forms.CharField(
        max_length=200,
        required=False)
    type_document_number = forms.CharField(
        max_length=200,
        required=False)
    telephone_number = forms.CharField(
        max_length=200,
        required=False)
    home_telephone_number = forms.CharField(
        max_length=200,
        required=False)

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
    
